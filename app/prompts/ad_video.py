"""广告行业 Seedance 2.0 请求示例（Swagger 下拉）。"""

from typing import Any

_TAOBAO_VIDEO = (
    "https://tbm-auth.alicdn.com/73bbe9f95b148212/bfa34f0de41b2f70/"
    "20240304_a6fb5e12d2975ac5_451659109152_96625244883166_published_mp4_264_hd_taobao.mp4"
    "?auth_key=1779656361-0-0-92e742543936211a464a9493f994a6a0"
    "&biz=tbs_vsucai-64598fb8d3bfd157"
    "&t=2147821817795963613143974e1254&w=720&h=720&e=hd"
    "&b=shopcenter&p=shopcenter_detail_pc&tr=mp4-264-hd&iss=false&v=taobao_v2"
)
_NECKLACE_IMAGE = (
    "https://img.alicdn.com/imgextra/i4/2217876692742/"
    "O1CN01pmB0e81W7t4XFlEZC_!!2217876692742.png"
)

AD_VIDEO_OPENAPI_EXAMPLES: dict[str, dict[str, Any]] = {
    "product_replace_necklace": {
        "summary": "商品替换 · 项链换品（文本+视频+图片）",
        "description": (
            "将参考视频中的商品替换为参考图中的粉色独角兽项链，运镜不变。"
            "参考视频须 2–15 秒。POST 秒回 task_id，再用 GET /api/v1/ad/video/{task_id} 轮询。"
        ),
        "value": {
            "mode": "product_replace",
            "prompt": (
                "将视频1中的商品替换成图片1中的粉色独角兽项链，"
                "运镜、镜头运动、节奏、构图完全不变，保持原电商广告质感与光影"
            ),
            "video_url": _TAOBAO_VIDEO,
            "image_url": _NECKLACE_IMAGE,
            "duration": 5,
            "ratio": "1:1",
            "resolution": "720p",
            "generate_audio": True,
            "watermark": False,
        },
    },
}
