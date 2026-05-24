# ad-ai

广告公司 AI 文案服务。API 只做转发，业务逻辑集中在 `services/`。

## 目录结构

```
app/
├── api/v1/endpoints/     # 薄接口层，只调 Service
├── schemas/              # 请求/响应模型
├── services/
│   ├── doubao.py         # 豆包对话底层（内部）
│   ├── seedream.py       # Seedream 图片生成底层（内部）
│   ├── seedance.py       # Seedance 视频生成底层（内部）
│   ├── ad_copy.py        # 广告文案业务
│   ├── ad_image.py       # 广告图片提效
│   └── ad_video.py       # 广告视频提效
├── prompts/              # LangChain 提示词模板
└── core/                 # 配置、日志
```

## 分层约定


| 层           | 职责                                        |
| ----------- | ----------------------------------------- |
| `endpoints` | 接收请求 → 调用 Service → 返回 `ApiResponse`      |
| `services`  | 业务逻辑、LangChain 组词、调用豆包                    |
| `prompts`   | 广告领域系统提示词（LangChain `ChatPromptTemplate`） |
| `doubao`    | 方舟对话 API，仅供 Service 依赖                  |
| `seedream`  | 方舟图片生成 API（Seedream 5.0 lite）            |


## 环境变量

```env
ARK_API_KEY=你的密钥
ARK_BASE_URL=https://ark.cn-beijing.volces.com

# 按能力分模型（控制台推理接入点 ID）
ARK_TEXT_MODEL=doubao-seed-2-0-lite-260428      # 文案 / 对话
ARK_IMAGE_MODEL=doubao-seedream-5-0-260128     # 图片 Seedream 5.0 lite
ARK_VIDEO_MODEL=doubao-seedance-2-0-260128     # 视频 Seedance 2.0
```

| 变量 | 用途 | 默认模型系列 |
|------|------|----------------|
| `ARK_TEXT_MODEL` | 广告文案、对话 | 豆包 Seed 文本 |
| `ARK_IMAGE_MODEL` | 广告主图、组图、图生图 | Seedream 5.0 lite |
| `ARK_VIDEO_MODEL` | 广告短视频、商品替换 | Seedance 2.0 |

图片能力见 [Seedream 5.0 lite API](https://www.volcengine.com/docs/82379/1541523?lang=zh)；三类能力共用 `ARK_API_KEY`。

## 启动

```bash
uv sync
cp .env.example .env   # 填入 ARK_API_KEY
uv run python main.py
```

文档：[http://localhost:8000/api/docs](http://localhost:8000/api/docs)

## 接口

### 健康检查

`GET /api/v1/health`

### 广告文案生成

`POST /api/v1/ad/copy`

```json
{
  "prompt": "品牌：某茶饮品牌\n产品：春季新品芝士莓莓\n人群：18-28岁女性\n卖点：新鲜草莓、芝士奶盖、限时第二杯半价\n调性：年轻、治愈\n渠道：微信公众号（推荐推文）\n场景：编辑推荐种草，引导领券",
  "count": 3
}
```

提示词里写明 **渠道：微信公众号** 时，会按订阅号推荐文结构生成（标题、短段落正文、引导点击/领券的 CTA）。

`model` 默认取 `ARK_TEXT_MODEL`，可在请求体覆盖。

### 广告图片生成（Seedream 5.0 lite）

`POST /api/v1/ad/image` · 流式 `POST /api/v1/ad/image/stream`（Swagger 请求体右上角可切换广告场景示例）

通过 `mode` 选择能力（对应控制台调试页签）：

| mode | 能力 | 广告典型场景 |
|------|------|----------------|
| `text_to_image` | 文生图 | 无素材，从 Brief 出信息流主图/KV 初稿 |
| `image_to_image` | 图生图 | 保产品/模特，换背景、换季节、换风格 |
| `multi_fusion` | 多图融合 | 模特+服装、产品+场景合成一张 |
| `multi_reference_group` | 多参考图生组图 | 同一品牌 VI 延展多张物料、剧情分镜组图 |

可选：`web_search: true` 开启联网搜索（热点/时效海报）；`max_images` 控制组图张数（1–15，且 参考图数+生成数≤15）。

**文生图 · 信息流主图**

```json
{
  "mode": "text_to_image",
  "prompt": "商业广告摄影，芝士莓莓茶饮，透明杯分层果泥与奶盖，明亮柔光、浅粉背景、留白加文案，竖版食欲感，无文字",
  "size": "2K",
  "watermark": false
}
```

**图生图 · 换节日背景**

```json
{
  "mode": "image_to_image",
  "prompt": "保持产品与构图不变，背景改为春节喜庆场景，红灯笼虚化，适合电商主图",
  "images": ["https://your-cdn.com/product.jpg"],
  "size": "2K"
}
```

**多图融合 · 穿搭合成**

```json
{
  "mode": "multi_fusion",
  "prompt": "将图1人物服装替换为图2款式，保持面部与姿态，时尚商业摄影",
  "images": ["https://your-cdn.com/model.jpg", "https://your-cdn.com/outfit.jpg"]
}
```

**多参考图生组图 · 品牌物料 pack**

```json
{
  "mode": "multi_reference_group",
  "prompt": "参考 Logo，生成户外运动品牌 GREEN 的帆布袋、帽子、会员卡、挂绳，统一绿色简约风，白底展示",
  "images": ["https://your-cdn.com/logo.png"],
  "max_images": 4,
  "size": "2K"
}
```

**联网搜索 · 热点借势**

```json
{
  "mode": "text_to_image",
  "prompt": "结合近期热门视觉，快消品促销海报，主视觉吸睛，预留标题区与价格条",
  "web_search": true,
  "size": "2K"
}
```

响应示例：

```json
{
  "mode": "text_to_image",
  "created": 1710000000,
  "images": [{ "url": "https://...", "revised_prompt": "" }],
  "usage": { "generated_images": 1 }
}
```

生成 URL 约 **24 小时**有效，请及时落库或转存 CDN。调试会产生真实计费，见[官方文档](https://www.volcengine.com/docs/82379/1541523?lang=zh)。

### 广告视频生成（Seedance 2.0）

`POST /api/v1/ad/video` · `GET /api/v1/ad/video/{task_id}` · Swagger 可切换「商品替换 · 项链换品」示例

多模态参考：**文本 + 参考视频 + 参考图**，用于电商「换品不换镜」——保持原片运镜，替换为新品图。见[创建视频生成任务 API](https://www.volcengine.com/docs/82379/1520757?lang=zh)。

**注意**：单段参考视频须 **2–15 秒**；过长会返回 400。参考图经服务端转 base64 上传，避免 CDN 403。

```json
POST /api/v1/ad/video
{
  "mode": "product_replace",
  "prompt": "将视频1中的商品替换成图片1中的粉色独角兽项链，运镜、镜头运动、节奏完全不变",
  "video_url": "https://.../product.mp4",
  "image_url": "https://.../necklace.png",
  "duration": 5,
  "ratio": "1:1",
  "resolution": "720p"
}
```

立即返回 `task_id`，再用 `GET /api/v1/ad/video/{task_id}` 轮询至 `status=succeeded`。成片 `video_url` 约 **24 小时**有效。

---

响应直接返回文案数组：

```json
[
  {
    "title": "标题",
    "body": "正文",
    "cta": "立即下单",
    "angle": "卖点突出"
  }
]
```



