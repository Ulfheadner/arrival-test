import json
from typing import Optional

from aiohttp import web
from bson import json_util, ObjectId


class EventsPaginator:
    DIRECTIONS_QUERIES = {
        "next": "$gt",
        "prev": "$lt",
    }

    def __init__(
        self,
        app: web.Application,
        page_size: int,
        url: str,
        direction: str,
        cursor: str,
    ):
        self._db = app["db"]
        self._page_size = page_size
        self._url = url
        self._direction = direction if direction in self.DIRECTIONS_QUERIES else "next"
        self._cursor = cursor

    def format_directions_links(self, direction: str, cursor: dict) -> Optional[str]:
        if cursor:
            return f"{self._url}?cursor={cursor['_id']['$oid']}&direction={direction}"
        return None

    def format_page(self, events: list) -> dict:
        next_cursor, prev_cursor = None, None

        if events:
            next_cursor, prev_cursor = events[-1], events[0]

        return {
            "count": len(events),
            "next_page": self.format_directions_links("next", next_cursor),
            "prev_page": self.format_directions_links("prev", prev_cursor),
            "events": events,
        }

    @staticmethod
    def serialize(mongo_object: dict) -> dict:
        return json.loads(json_util.dumps(mongo_object))

    def _get_mongo_ordering(self) -> int:
        if self._direction == "prev":
            return -1
        return 1

    async def get_events(self, condition: dict, ordering: int = 1) -> list:
        query = (
            self._db.events.find(condition)
            .sort("_id", ordering)
            .limit(self._page_size)
            .sort("_id", 1)
        )
        return [
            self.serialize(result)
            for result in await query.to_list(length=self._page_size)
        ]

    async def get_page(self) -> dict:
        condition = {}
        ordering = self._get_mongo_ordering()
        if self._cursor is not None:
            condition = {
                "_id": {
                    self.DIRECTIONS_QUERIES[self._direction]: ObjectId(self._cursor)
                }
            }
        events = await self.get_events(condition, ordering)
        return self.format_page(events)
