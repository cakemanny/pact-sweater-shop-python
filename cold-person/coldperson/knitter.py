import logging
import os
from dataclasses import asdict, dataclass
from typing import Any, Optional
import json

import aiohttp

logger = logging.getLogger(__name__)

# we probably ought to use attrs ...


@dataclass
class SweaterOrder:
    colour: str
    order_number: int

    @classmethod
    def from_dict(cls, d: dict[str, Any]):
        match d:
            case {
                "colour": str(colour),
                "order_number": int(order_number),
            }:
                return cls(colour, order_number)
        raise ValueError


@dataclass
class Sweater:
    colour: str
    order_number: int

    def to_dict(self):
        return asdict(self)


class Knitter:
    """
    A Client for the Knitter Service
    """

    def __init__(self, session: aiohttp.client.ClientSession) -> None:
        self.session = session

    def _endpoint(self, p: str) -> str:
        base_url = os.getenv("KNITTER_BASE_URL", "http://localhost:1234")
        assert base_url
        return f"{base_url}{p}"

    async def get_sweater(self, order: SweaterOrder) -> Sweater:
        request_data = json.dumps({
            "colour": order.colour,
            "order_number": order.order_number,
        })
        async with self.session.post(
            self._endpoint("/sweater/order"),
            headers={'Content-Type': 'application/json'},
            data=request_data,
        ) as resp:
            if resp.status >= 400:
                try:
                    body = await resp.text()
                except Exception:
                    body = None
                logger.error('%s', json.dumps({
                    'message': 'Placing order failed',
                    'resp': str(resp),
                    'body': str(body)
                }))
                raise Exception('Error placing order with knitter')
            data = await resp.json()
            return Sweater(data["colour"], data["order_number"])
