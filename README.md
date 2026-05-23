# ad-ai

广告公司 AI 文案服务。API 只做转发，业务逻辑集中在 `services/`。

## 目录结构

```
app/
├── api/v1/endpoints/     # 薄接口层，只调 Service
├── schemas/              # 请求/响应模型
├── services/
│   ├── doubao.py         # 豆包底层调用（内部使用，不对外暴露）
│   └── ad_copy.py        # 广告文案业务
├── prompts/              # LangChain 提示词模板
└── core/                 # 配置、日志
```

## 分层约定


| 层           | 职责                                        |
| ----------- | ----------------------------------------- |
| `endpoints` | 接收请求 → 调用 Service → 返回 `ApiResponse`      |
| `services`  | 业务逻辑、LangChain 组词、调用豆包                    |
| `prompts`   | 广告领域系统提示词（LangChain `ChatPromptTemplate`） |
| `doubao`    | 方舟 HTTP，仅供 Service 依赖                     |


## 环境变量

```env
ARK_API_KEY=你的密钥
ARK_BASE_URL=https://ark.cn-beijing.volces.com
ARK_DEFAULT_MODEL=doubao-seed-2-0-lite-260428
```

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

`model` 默认取 `ARK_DEFAULT_MODEL`，可在请求体覆盖。

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



