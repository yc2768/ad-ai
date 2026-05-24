import uvicorn

from app.core.config import settings


def main() -> None:
    print(f"API docs  | {settings.base_url}/api/docs")
    print(f"Health    | {settings.base_url}/api/v1/health")
    print(f"Ad copy   | POST {settings.base_url}/api/v1/ad/copy")
    print(f"Ad image  | POST {settings.base_url}/api/v1/ad/image")
    print(f"Ad video  | POST {settings.base_url}/api/v1/ad/video")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
