"""Swagger / ReDoc 静态资源（避免默认 jsdelivr 在部分网络下白屏）。"""

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

# BootCDN 在国内与 IDE 内置浏览器中比 jsdelivr 更稳定
SWAGGER_UI_CSS = (
    "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.11.0/swagger-ui.css"
)
SWAGGER_UI_JS = (
    "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.11.0/swagger-ui-bundle.js"
)
REDOC_JS = "https://cdn.bootcdn.net/ajax/libs/redoc/2.1.3/bundles/redoc.standalone.js"


def register_doc_routes(app: FastAPI, *, title: str, openapi_url: str) -> None:
    @app.get("/api/docs", include_in_schema=False)
    async def swagger_ui() -> object:
        return get_swagger_ui_html(
            openapi_url=openapi_url,
            title=f"{title} - Swagger UI",
            swagger_css_url=SWAGGER_UI_CSS,
            swagger_js_url=SWAGGER_UI_JS,
        )

    @app.get("/api/redoc", include_in_schema=False)
    async def redoc_ui() -> object:
        return get_redoc_html(
            openapi_url=openapi_url,
            title=f"{title} - ReDoc",
            redoc_js_url=REDOC_JS,
        )
