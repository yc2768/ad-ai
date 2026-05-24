"""广告行业 Seedream 请求示例（Swagger 请求体下拉）。"""

from typing import Any

AD_IMAGE_OPENAPI_EXAMPLES: dict[str, dict[str, Any]] = {
    "text_to_image_feed": {
        "summary": "文生图 · 信息流主图",
        "description": (
            "无素材，从 Brief 出 2K 竖版主图（抖音/小红书信息流）。"
            "Brief 写清品牌、卖点、留白区；水印关闭便于后期加字。"
        ),
        "value": {
            "mode": "text_to_image",
            "prompt": (
                "商业广告摄影，某茶饮品牌春季新品芝士莓莓，"
                "透明杯身分层草莓果泥与芝士奶盖，新鲜草莓点缀，"
                "明亮柔光、浅粉背景、留白适合叠加价格与 CTA，"
                "竖版 3:4 构图，高质感、食欲感，无文字"
            ),
            "size": "2K",
            "watermark": False,
        },
    },
    "image_to_image_season": {
        "summary": "图生图 · 换节日背景",
        "description": (
            "保产品/构图，改背景氛围。适合电商主图节日改版；"
            "参考图需清晰、主体居中。"
        ),
        "value": {
            "mode": "image_to_image",
            "prompt": (
                "保持产品与构图不变，将背景改为春节喜庆场景，"
                "红灯笼与金色光斑虚化，暖色高光，仍适合电商主图，"
                "专业广告修图质感"
            ),
            "images": [
                "https://img.alicdn.com/img/i1/17794749/O1CN01kGeV5r1kx62XHLgha_!!4611686018427381437-0-saturn_solar.jpg"
            ],
            "size": "2K",
            "watermark": False,
        },
    },
    "multi_fusion_outfit": {
        "summary": "多图融合 · 模特穿搭",
        "description": (
            "人物定妆照 + 服装平铺，合成种草穿搭图。"
            "提示词写清图1=人物、图2=服装；需 2–14 张参考图。"
        ),
        "value": {
            "mode": "multi_fusion",
            "prompt": (
                "将图1人物的服装替换为图2的服装款式与颜色，"
                "保持人物姿态与面部不变，自然褶皱与光影，"
                "时尚杂志级商业摄影"
            ),
            "images": [
                "https://asearch.alicdn.com/bao/uploaded/O1CN01QubNxd1hmc3KdcRK8_!!2212020164320.jpg",
                "https://asearch.alicdn.com/bao/uploaded/O1CN01B8n7nr1oVOOOqs1CC_!!3249895230.jpg",
            ],
            "size": "2K",
            "watermark": False,
        },
    },
    "multi_reference_brand_pack": {
        "summary": "多参考图生组图 · 品牌物料",
        "description": (
            "基于 Logo 一次出帆布袋、帽子、卡片等同风格物料，适合提案 pack。"
            "max_images 按物料数量设置；参考图+生成数≤15。"
        ),
        "value": {
            "mode": "multi_reference_group",
            "prompt": (
                "参考品牌 Logo，生成一套户外运动品牌「GREEN」视觉物料："
                "帆布袋、棒球帽、会员卡、挂绳，统一绿色主色与简约线条，"
                "白底产品展示，适合提案 PPT"
            ),
            "images": ["https://example.com/brand-logo.png"],
            "max_images": 4,
            "size": "2K",
            "watermark": False,
        },
    },
    "text_to_image_web_search": {
        "summary": "文生图 · 联网搜索（热点借势）",
        "description": (
            "结合实时热点/IP 做时效海报；仅 Seedream 5.0 lite 支持 web_search。"
            "适合节日、赛事、爆款借势。"
        ),
        "value": {
            "mode": "text_to_image",
            "prompt": (
                "结合近期热门视觉元素，设计一张快消品促销海报，"
                "主视觉吸睛、适合朋友圈传播，预留顶部标题区与底部价格条，"
                "现代扁平插画风格"
            ),
            "size": "2K",
            "web_search": True,
            "watermark": False,
        },
    },
    "multi_reference_storyboard": {
        "summary": "多参考图生组图 · 剧情分镜",
        "description": (
            "一次出 3 张连贯场景，用于短视频封面或 carousel。"
            "写清张数与情绪递进；参考图+生成数≤15。"
        ),
        "value": {
            "mode": "multi_reference_group",
            "prompt": (
                "生成3张同一女孩与品牌吉祥物在游乐园坐过山车的连贯插画，"
                "情绪递进：期待、尖叫、开心，统一日系明亮配色，适合横滑广告"
            ),
            "images": ["https://example.com/character-ref.jpg"],
            "max_images": 3,
            "size": "16:9",
            "watermark": False,
        },
    },
}
