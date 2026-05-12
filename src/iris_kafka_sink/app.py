import structlog

from iris_kafka_sink import __version__
from iris_kafka_sink.config.schema import AppConfig
from iris_kafka_sink.observability.logging_setup import configure_logging

logger = structlog.get_logger(__name__)


class Application:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def run(self) -> int:
        configure_logging(self.config.logging)
        logger.info("started", version=__version__, service_name=self.config.service.name)
        return 0
