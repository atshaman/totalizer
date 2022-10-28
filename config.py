import attrs

"""Класс для работы с конфигурацией """


@attrs.define(kw_only=True)
class Kafka:
    bootstrap: str
    topic: str = "nifi-data"
    instances: int = 1


@attrs.define(kw_only=True)
class Redis:
    host: str
    port: int = 6379
    db: str = "db0"


@attrs.define(kw_only=True)
class Keycloak:
    host: str = "keycloak.ziiot.svc"
    client_id: str
    client_secret: str


@attrs.define
class Metadata:
    metadataurl: str = "zif-rtdb-metadata.ziiot.svc"


@attrs.define(kw_only=True)
class Service:
    interface: str = "0.0.0.0"
    port: int = 8080
    context: str = "/"


class Config:
    """Синглтон с конфигурацией"""

    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self, kafka, redis, keycloak, metadata, service):
        self.kafka = kafka
        self.redis = redis
        self.keycloak = keycloak
        self.metadata = metadata
        self.service = service


if __name__ == "__main__":
    pass
