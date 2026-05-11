import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

from iris_kafka_sink.config.errors import ConfigError
from iris_kafka_sink.config.schema import AppConfig


def load_config(path: str | Path) -> AppConfig:
    """Load the application configuration from a YAML file"""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if raw is None:
        raise ConfigError(f"Configuration file {path} is empty")

    _substitute_secrets(AppConfig, raw)
    return AppConfig.model_validate(raw)


def _substitute_secrets(
    model_cls: type[BaseModel], raw_section: dict[str, Any] | None, path: str = ""
) -> None:
    """Recursively substitute secret-field values from environment variables."""
    if not isinstance(raw_section, dict):
        return

    for field_name, field_info in model_cls.model_fields.items():
        annotation = field_info.annotation

        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            # Recurse into nested sections
            _substitute_secrets(annotation, raw_section.get(field_name), f"{path}{field_name}.")
        elif field_name.endswith("_env"):
            if not (env_var_name := raw_section.get(field_name)):
                continue
            if (env_var_value := os.environ.get(env_var_name)) is None:
                raise ConfigError(
                    f"Environment variable {env_var_name} is not set "
                    f"(referenced by {path}{field_name})"
                )
            # Replace the field value with the environment variable value
            raw_section[field_name.removesuffix("_env")] = env_var_value
