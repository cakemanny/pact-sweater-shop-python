import json
import logging
import os
from dataclasses import asdict, dataclass
from typing import NoReturn

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class Hat:
    colour: str
    order_number: int
    material: str

    def to_dict(self):
        return asdict(self)


class Hatter:
    """
    A client for the Hatter service
    """

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session
        self.auth = aiohttp.BasicAuth("cold-person", "im-a-freezin")

    def _endpoint(self, path: str) -> str:
        base_url = os.getenv("HATTER_BASE_URL", "http://localhost:8081")
        assert base_url
        return f"{base_url}{path}"

    async def get_hat(self, order) -> Hat:
        async with self.session.post(
            self._endpoint("/hat/order"),
            auth=self.auth,
            json=order,
        ) as resp:
            if resp.status >= 400:
                await self._handle_bad_request(resp)
            data = await resp.json()
            return Hat(**data)

    async def _handle_bad_request(self, resp: aiohttp.ClientResponse) -> NoReturn:
        logger.error(
            "%s",
            json.dumps(
                {
                    "message": "Placing hat order failed",
                    "method": str(resp.request_info.method),
                    "endpoint": str(resp.request_info.real_url),
                    "resp": str(resp),
                    "resp_body": await resp.text(),
                }
            ),
        )
        raise Exception("Error placing order with Hatter")
