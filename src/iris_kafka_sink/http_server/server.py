import threading

import uvicorn
from fastapi import FastAPI

from iris_kafka_sink.config.schema import HttpConfig
from iris_kafka_sink.http_server.health import create_router
from iris_kafka_sink.http_server.state import HealthState


class HttpServer:
    def __init__(self, cfg: HttpConfig, state: HealthState) -> None:
        app = FastAPI()
        app.include_router(create_router(state))

        config = uvicorn.Config(
            app,
            host=cfg.host,
            port=cfg.port,
            log_config=None,
            access_log=False,
        )
        self._server = uvicorn.Server(config)
        self._thread = threading.Thread(
            target=self._server.run,
            name="http-server",
            daemon=True,
        )

    def start(self) -> None:
        self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=timeout)
