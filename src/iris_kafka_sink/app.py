import logging

from iris_kafka_sink import __version__

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, config_path: str, validate_only: bool = False) -> None:
        self.config_path = config_path
        self.validate_only = validate_only

    def run(self) -> int:
        logger.info("started", extra={"version": __version__, "config_path": self.config_path})
        return 0
