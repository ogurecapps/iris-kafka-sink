import argparse
import sys
from collections.abc import Sequence

import yaml
from pydantic import ValidationError

from iris_kafka_sink import __version__
from iris_kafka_sink.app import Application
from iris_kafka_sink.config.errors import ConfigError
from iris_kafka_sink.config.loader import load_config


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

    try:
        cfg = load_config(args.config)
    except (ConfigError, ValidationError, yaml.YAMLError, FileNotFoundError) as e:
        print(f"iris-kafka-sink: error: {e}", file=sys.stderr)
        return 1
    if args.validate_config:
        print(f"iris-kafka-sink: configuration is valid: {args.config}")
        return 0

    app = Application(config=cfg)
    return app.run()
