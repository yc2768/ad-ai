from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None


class HealthData(BaseModel):
    status: str = "ok"
    app_name: str
    version: str
