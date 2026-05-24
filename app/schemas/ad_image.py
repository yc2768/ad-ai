from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator

from app.core.config import settings


class AdImageMode(str, Enum):
    """Seedream 5.0 lite 创作模式。"""

    TEXT_TO_IMAGE = "text_to_image"
    IMAGE_TO_IMAGE = "image_to_image"
    MULTI_FUSION = "multi_fusion"
    MULTI_REFERENCE_GROUP = "multi_reference_group"


class AdImageRequest(BaseModel):
    mode: AdImageMode = Field(
        default=AdImageMode.TEXT_TO_IMAGE,
        description="文生图 / 图生图 / 多图融合 / 多参考图生组图",
    )
    prompt: str = Field(
        ...,
        min_length=1,
        description="画面描述或编辑指令（广告场景：主体、卖点、调性、尺寸用途）",
    )
    images: list[str] = Field(
        default_factory=list,
        description="参考图 URL 列表（图生图 1 张；多图融合 2–14 张；组图 1–14 张）",
    )
    size: str = Field(
        default="2K",
        description='输出尺寸，如 "2K"、"3K"、"16:9"、"2048x2048"',
    )
    max_images: int = Field(
        default=4,
        ge=1,
        le=15,
        description="组图模式最多生成张数（参考图数量 + 生成张数 ≤ 15）",
    )
    web_search: bool = Field(
        default=False,
        description="联网搜索（仅 Seedream 5.0 lite，适合热点/时效素材）",
    )
    watermark: bool = Field(default=False, description="是否添加「AI生成」水印")
    model: str = Field(
        default=settings.ark_image_model,
        description="图片生成模型 ID，默认 ARK_IMAGE_MODEL",
        examples=["doubao-seedream-5-0-260128"],
    )

    @field_validator("images")
    @classmethod
    def strip_images(cls, value: list[str]) -> list[str]:
        return [u.strip() for u in value if u and u.strip()]

    @model_validator(mode="after")
    def validate_mode_inputs(self) -> "AdImageRequest":
        if self.mode == AdImageMode.TEXT_TO_IMAGE and self.images:
            raise ValueError("文生图模式不需要参考图，请移除 images")
        if self.mode == AdImageMode.IMAGE_TO_IMAGE and len(self.images) != 1:
            raise ValueError("图生图模式需要且仅需 1 张参考图")
        if self.mode == AdImageMode.MULTI_FUSION and len(self.images) < 2:
            raise ValueError("多图融合模式需要至少 2 张参考图")
        if self.mode == AdImageMode.MULTI_REFERENCE_GROUP and not self.images:
            raise ValueError("多参考图生组图模式需要至少 1 张参考图")
        if len(self.images) > 14:
            raise ValueError("参考图最多 14 张")
        if self.max_images + len(self.images) > 15:
            raise ValueError("参考图数量 + 生成张数不能超过 15")
        return self


class AdImageItem(BaseModel):
    url: str = ""
    b64_json: str = ""
    revised_prompt: str = ""


class AdImageResponse(BaseModel):
    mode: AdImageMode
    created: int | None = None
    images: list[AdImageItem]
    usage: dict | None = None
