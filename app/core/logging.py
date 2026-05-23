import logging
import sys
from logging.handlers import RotatingFileHandler

from app.core.config import settings


def setup_logging() -> None:
    """Configure root logger: console + rotating file."""
    settings.log_dir.mkdir(parents=True, exist_ok=True)

    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    root = logging.getLogger()
    root.setLevel(settings.log_level.upper())

    if root.handlers:
        root.handlers.clear()

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    file_handler = RotatingFileHandler(
        settings.log_dir / "app.log",
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
