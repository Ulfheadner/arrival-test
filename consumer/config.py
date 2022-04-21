import os
from dataclasses import dataclass


@dataclass
class Config:
    MONGO_URL: str
    VEHICLE_WS_URL: str
    HOST: str
    PORT: int
    PAGE_SIZE: int


def load_from_env() -> Config:
    return Config(
        MONGO_URL=os.environ.get("MONGO_URL", "mongodb://root:example@mongo:27017"),
        VEHICLE_WS_URL=os.environ.get("MONGO_URL", "ws://vehicle_emulator:8080"),
        HOST=os.environ.get("HOST", "0.0.0.0"),
        PORT=os.environ.get("PORT", "8000"),
        PAGE_SIZE=os.environ.get("PAGE_SIZE", 50),
    )
