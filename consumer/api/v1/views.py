from typing import Optional

from aiohttp import web

from .paginators import EventsPaginator


async def events_view(request: web.Request):
    page_size: int = request.app["settings"].PAGE_SIZE
    cursor: Optional[str] = request.query.get("cursor")
    direction: Optional[str] = request.query.get("direction", "next").lower()

    paginator = EventsPaginator(
        app=request.app,
        page_size=page_size,
        url=request.path,
        direction=direction,
        cursor=cursor,
    )
    prepared_page = await paginator.get_page()

    return web.json_response(data=prepared_page)
