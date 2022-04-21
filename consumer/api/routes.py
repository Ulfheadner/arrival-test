from aiohttp import web

from .v1.views import events_view


def init_routes(app: web.Application):
    app.router.add_get("/events", events_view, name="events")
