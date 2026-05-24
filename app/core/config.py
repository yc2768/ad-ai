from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ad-ai"
    app_version: str = "0.1.0"
    debug: bool = False

    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def display_host(self) -> str:
        if self.host in ("0.0.0.0", "::"):
            return "localhost"
        return self.host

    @property
    def base_url(self) -> str:
        return f"http://{self.display_host}:{self.port}"

    log_level: str = "INFO"
    log_dir: Path = Field(default=PROJECT_ROOT / "logs")
    log_max_bytes: int = 10 * 1024 * 1024
    log_backup_count: int = 5

    # 火山方舟 / 豆包（按能力分模型，值为控制台推理接入点 ID）
    ark_api_key: str | None = None
    ark_base_url: str = "https://ark.cn-beijing.volces.com"
    ark_text_model: str = "doubao-seed-2-0-lite-260428"
    ark_image_model: str = "doubao-seedream-5-0-260128"
    ark_video_model: str = "doubao-seedance-2-0-260128"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
