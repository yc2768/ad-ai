from enum import Enum

from pydantic import BaseModel, Field, model_validator

from app.core.config import settings


class AdVideoMode(str, Enum):
    """Seedance 2.0 广告视频模式。"""

    PRODUCT_REPLACE = "product_replace"


class AdVideoRequest(BaseModel):
    mode: AdVideoMode = Field(
        default=AdVideoMode.PRODUCT_REPLACE,
        description="商品替换：参考视频 + 参考图 + 文本指令",
    )
    prompt: str = Field(
        ...,
        min_length=1,
        description="编辑指令，建议写明「视频1」「图片1」及「运镜不变」",
    )
    video_url: str = Field(..., description="参考视频 URL（单段 2–15 秒，mp4）")
    image_url: str = Field(..., description="替换后的商品/主体参考图 URL")
    duration: int = Field(
        default=5,
        ge=4,
        le=15,
        description="生成视频时长（秒）",
    )
    ratio: str = Field(
        default="1:1",
        description='画幅，如 "1:1"、"16:9"、"9:16"、"adaptive"',
    )
    resolution: str = Field(default="720p", description='分辨率：480p / 720p / 1080p')
    generate_audio: bool = Field(default=True, description="是否生成配套音频（Seedance 原生音画同出）")
    watermark: bool = Field(default=False, description="是否添加水印")
    model: str = Field(
        default=settings.ark_video_model,
        description="视频模型 ID，默认 ARK_VIDEO_MODEL",
        examples=["doubao-seedance-2-0-260128"],
    )

    @model_validator(mode="after")
    def validate_urls(self) -> "AdVideoRequest":
        for name, url in (("video_url", self.video_url), ("image_url", self.image_url)):
            if not url.strip().startswith(("http://", "https://")):
                raise ValueError(f"{name} 必须是可访问的 http(s) URL")
        return self


class AdVideoResponse(BaseModel):
    mode: AdVideoMode
    task_id: str
    status: str
    video_url: str = ""
    usage: dict | None = None
    message: str = ""
