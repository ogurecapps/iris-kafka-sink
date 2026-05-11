from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class _StrictBase(BaseModel):
    """Base for all config models — forbids extra fields."""
    model_config = ConfigDict(extra="forbid")

class ProcessingConfig(_StrictBase):
    batch_size: int = Field(default=1000, ge=1)
    retry_backoff_initial_ms: int = Field(default=1000, ge=1)
    retry_backoff_multiplier: float = Field(default=2.0, gt=1.0)
    retry_backoff_max_ms: int = Field(default=60000, ge=1)

class ProtobufConfig(_StrictBase):
    module: str
    message_class: str

class LoggingConfig(_StrictBase):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    format: Literal["json", "console"] = "json"

class ServiceConfig(_StrictBase):
    name: str

class HttpConfig(_StrictBase):
    host: str = "0.0.0.0"
    port: int = Field(default=8080, ge=1, le=65535)