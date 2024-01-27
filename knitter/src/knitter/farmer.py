import json
import logging
import os
from typing import Optional

import aiohttp
from attr import asdict, define, field, validators

logger = logging.getLogger(__name__)


@define
class WoolOrder:
    colour: str = field(validator=validators.instance_of(str))
    order_number: int = field(validator=validators.instance_of(int))


@define
class Skein:
    colour: str = field(validator=validators.instance_of(str))
    weight: Optional[str] = None


class Farmer:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session

    def endpoint(self, path: str):
        base_url = os.getenv("FARMER_BASE_URL", "http://localhost:8082")
        assert base_url
        return f"{base_url}{path}"

    async def get_wool(self, order: WoolOrder) -> Skein:
        async with self.session.post(
            self.endpoint("/wool/order"),
            json=asdict(order),
        ) as resp:
            if not resp.ok:
                logger.error(
                    "%s",
                    json.dumps(
                        {
                            "message": "Placing order failed",
                            "resp": str(resp),
                            "body": await resp.text(),
                        }
                    ),
                )
                raise Exception("Error placing order with knitter")
            data = await resp.json()
            return Skein(data["colour"], data.get("weight"))
