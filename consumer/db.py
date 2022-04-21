import logging

from aiohttp import web

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


async def init_mongo(app: web.Application):
    client = AsyncIOMotorClient(app["settings"].MONGO_URL)
    app["db"] = client["vehicle"]


async def insert(app: web.Application, data: dict) -> None:
    try:
        await app["db"].events.insert_one(data)
    except PyMongoError as ex:
        # TODO: добавить временное хранение сообщений, если не удалось сохранить в монгу
        logging.error(f"Insert failed. {ex}")
