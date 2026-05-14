from dataclasses import dataclass


@dataclass
class HealthState:
    kafka_connected: bool = False
    schema_registry_connected: bool = False
    iris_connected: bool = False

    def snapshot(self) -> dict[str, bool]:
        return {
            "kafka": self.kafka_connected,
            "schema_registry": self.schema_registry_connected,
            "iris": self.iris_connected,
        }
