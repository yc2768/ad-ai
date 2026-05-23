from pydantic import BaseModel, Field

from app.core.config import settings

DEFAULT_AD_COPY_PROMPT = (
    "品牌：某茶饮品牌\n"
    "产品：春季新品芝士莓莓\n"
    "人群：18-28岁女性\n"
    "卖点：新鲜草莓、芝士奶盖、限时第二杯半价\n"
    "调性：年轻、治愈、像朋友安利\n"
    "渠道：微信公众号（订阅号推荐推文/种草）\n"
    "场景：公众号编辑推荐一篇新品软文，引导读者领券下单"
)


class AdCopyRequest(BaseModel):
    prompt: str = Field(
        default=DEFAULT_AD_COPY_PROMPT,
        description="输入提示词（品牌、产品、人群、卖点、调性、渠道等可写在一起）",
        min_length=1,
    )
    count: int = Field(default=3, ge=1, le=10, description="生成方案数量")
    model: str = Field(
        default=settings.ark_default_model,
        description="豆包模型 ID，默认读取环境变量 ARK_DEFAULT_MODEL",
        examples=["doubao-seed-2-0-lite-260428"],
    )


class AdCopyItem(BaseModel):
    title: str = ""
    body: str
    cta: str = ""
    angle: str = ""
