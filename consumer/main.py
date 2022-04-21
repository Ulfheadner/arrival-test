import logging
from aiohttp import web

from db import init_mongo
from config import Config, load_from_env
from api.routes import init_routes
from websoket_listener import start_listener, stop_listener

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


async def start_background_tasks(app: web.Application) -> None:
    await start_listener(app)


async def cleanup_background_tasks(app: web.Application) -> None:
    await stop_listener(app)


async def init_app(settings: Config) -> web.Application:
    app = web.Application()
    app["settings"] = settings

    app.on_startup.append(init_mongo)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    init_routes(app)

    return app


if __name__ == "__main__":
    config = load_from_env()
    web.run_app(app=init_app(config), host=config.HOST, port=config.PORT)
