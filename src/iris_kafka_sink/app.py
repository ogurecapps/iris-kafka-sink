import logging

from iris_kafka_sink import __version__
from iris_kafka_sink.config.schema import AppConfig

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def run(self) -> int:
        logger.info(
            "started", extra={"version": __version__, "service_name": self.config.service.name}
        )
        return 0
