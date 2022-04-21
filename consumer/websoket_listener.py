import time
import json

import asyncio
import websockets
import logging
from aiohttp import web

from db import insert

logger = logging.getLogger("websockets")
logger.setLevel(logging.INFO)

DEFAULT_VALUES = {
    "country": "USA",
}


def set_default(data: dict) -> dict:
    data["created_at"] = time.time()
    for key, value in DEFAULT_VALUES.items():
        if data.get(key) is None:
            data[key] = value

    return data


async def save(app: web.Application, message: bytes):
    try:
        data = json.loads(message)
        await insert(app, set_default(data))
    except json.JSONDecodeError as ex:
        logger.debug(f"Wrong json. Error message: {ex.msg}")


async def handler(
    websocket: websockets.WebSocketClientProtocol, app: web.Application
) -> None:
    async for message in websocket:
        try:
            await save(app, message)
        except Exception as ex:
            # Catch all exceptions for protecting of reading from socket
            logger.error(f"Unhandled error: {ex}")


async def consume(app: web.Application) -> None:
    async for websocket in websockets.connect(app["settings"].VEHICLE_WS_URL):
        try:
            await handler(websocket, app)
        except websockets.ConnectionClosed:
            # Websockets library adds message to logger and retries to connect
            continue


async def start_listener(app: web.Application):
    app["vehicle_listener"] = asyncio.create_task(consume(app))


async def stop_listener(app: web.Application):
    app["vehicle_listener"].cancel()
    await app["vehicle_listener"]
