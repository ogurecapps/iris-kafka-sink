import argparse
import logging
from collections.abc import Sequence

from iris_kafka_sink import __version__
from iris_kafka_sink.app import Application


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="iris-kafka-sink",
        description="Stream Kafka messages into InterSystems IRIS.",
    )
    parser.add_argument(
        "--config",
        default="./config.yaml",
        help="Path to YAML config file (default: ./config.yaml).",
    )
    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Load and validate config, then exit.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    app = Application(config_path=args.config, validate_only=args.validate_config)
    return app.run()
