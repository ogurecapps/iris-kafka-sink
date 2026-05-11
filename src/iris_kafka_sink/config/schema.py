import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_IRIS_CLASS_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*(\.[A-Za-z][A-Za-z0-9]*)+$")


class _StrictBase(BaseModel):
    """Base for all config models — forbids extra fields."""

    model_config = ConfigDict(extra="forbid")


class IrisConfig(_StrictBase):
    hostname: str
    port: int = Field(default=1972, ge=1, le=65535)
    namespace: str
    username: str
    password_env: str
    target_class: str
    connection_timeout_s: int = Field(default=10, ge=1)

    @field_validator("target_class")
    @classmethod
    def _check_class_format(cls, v: str) -> str:
        if not _IRIS_CLASS_RE.match(v):
            raise ValueError(f"invalid target_class format: {v!r}")
        return v


class SchemaRegistryConfig(_StrictBase):
    url: str
    subject: str
    basic_auth_user: str | None = None
    basic_auth_password_env: str | None = None

    @model_validator(mode="after")
    def _validate_basic_auth(self) -> "SchemaRegistryConfig":
        user_set = self.basic_auth_user is not None
        pwd_set = self.basic_auth_password_env is not None
        if user_set != pwd_set:
            raise ValueError(
                "basic_auth_user and basic_auth_password_env must be set together or both omitted"
            )
        return self


class KafkaSecurityConfig(_StrictBase):
    protocol: Literal["PLAINTEXT", "SASL_SSL"] = "PLAINTEXT"
    sasl_mechanism: Literal["PLAIN", "SCRAM-SHA-256", "SCRAM-SHA-512"] | None = None
    sasl_username: str | None = None
    sasl_password_env: str | None = None
    ssl_ca_location: str | None = None

    @model_validator(mode="after")
    def _validate_security_config(self) -> "KafkaSecurityConfig":
        if self.protocol == "SASL_SSL":
            if not self.sasl_mechanism:
                raise ValueError("sasl_mechanism is required when protocol is SASL_SSL")
            if not self.sasl_username:
                raise ValueError("sasl_username is required when protocol is SASL_SSL")
            if not self.sasl_password_env:
                raise ValueError("sasl_password_env is required when protocol is SASL_SSL")
        return self


class KafkaConfig(_StrictBase):
    bootstrap_servers: str
    topic: str
    group_id: str
    auto_offset_reset: Literal["earliest", "latest"] = "earliest"
    poll_timeout_ms: int = Field(default=1000, ge=1)
    max_poll_records: int = Field(default=500, ge=1)
    session_timeout_ms: int = Field(default=30000, ge=1000)
    security: KafkaSecurityConfig = Field(default_factory=KafkaSecurityConfig)


class ProcessingConfig(_StrictBase):
    batch_size: int = Field(default=500, ge=1)
    retry_backoff_initial_ms: int = Field(default=1000, ge=1)
    retry_backoff_multiplier: float = Field(default=2.0, gt=1.0)
    retry_backoff_max_ms: int = Field(default=60000, ge=1)

    @model_validator(mode="after")
    def _check_backoff_consistency(self) -> "ProcessingConfig":
        if self.retry_backoff_max_ms < self.retry_backoff_initial_ms:
            raise ValueError(
                f"retry_backoff_max_ms ({self.retry_backoff_max_ms}) must be >= "
                f"retry_backoff_initial_ms ({self.retry_backoff_initial_ms})"
            )
        return self


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


class AppConfig(_StrictBase):
    service: ServiceConfig
    kafka: KafkaConfig
    schema_registry: SchemaRegistryConfig
    protobuf: ProtobufConfig
    iris: IrisConfig
    processing: ProcessingConfig = Field(default_factory=ProcessingConfig)
    http: HttpConfig = Field(default_factory=HttpConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
