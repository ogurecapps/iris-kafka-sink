import structlog

from iris_kafka_sink import __version__
from iris_kafka_sink.config.schema import AppConfig
from iris_kafka_sink.http_server.server import HttpServer
from iris_kafka_sink.http_server.state import HealthState
from iris_kafka_sink.observability.logging_setup import configure_logging

logger = structlog.get_logger(__name__)


# How to run:
# export IRIS_PASSWORD=foo
# iris-kafka-sink --config config/example.yaml
# Before committing changes: ruff check --fix src/ && ruff format src/
class Application:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.state = HealthState()
        self.http = HttpServer(self.config.http, self.state)

    def run(self) -> int:
        configure_logging(self.config.logging)
        logger.info("started", version=__version__, service_name=self.config.service.name)
        self.http.start()
        try:
            self.http._thread.join()
        except KeyboardInterrupt:
            pass
        finally:
            self.http.stop()
        return 0
