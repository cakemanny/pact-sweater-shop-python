import logging
from enum import Enum

import aiohttp
from aiohttp import web
from attr import asdict, define, field, validators

from knitter.farmer import Farmer, WoolOrder


routes = web.RouteTableDef()
logger = logging.getLogger(__name__)

session_key = web.AppKey("session", aiohttp.ClientSession)


@define
class SweaterOrder:
    colour: str = field(validator=validators.instance_of(str))
    order_number: int = field(validator=validators.instance_of(int))


class Style(str, Enum):
    LONG_SLEEVED = "long_sleeved"
    SHORT_SLEEVED = "short_sleeved"

    def __str__(self) -> str:
        return str.__str__(self)


@define
class Sweater:
    colour: str = field(validator=validators.instance_of(str))
    order_number: int = field(validator=validators.instance_of(int))
    style: Style = Style.LONG_SLEEVED


@routes.post("/sweater/order")
async def knit_sweater(request: web.Request) -> web.Response:
    order_data = await request.json()
    sweater_order = SweaterOrder(
        order_data.get("colour"), order_data.get("order_number")
    )

    farmer = Farmer(request.app[session_key])

    skein = await farmer.get_wool(
        WoolOrder(sweater_order.colour, sweater_order.order_number)
    )

    sweater = Sweater(skein.colour, order_number=sweater_order.order_number)

    return web.json_response(asdict(sweater))


@routes.get("/healthz")
async def healthz(request: web.Request) -> web.Response:
    print(type(request))
    return web.Response(status=200, text="everything's gravy baby\n")


async def app_session(app: web.Application):
    # Use one session for the life of the app
    async with aiohttp.ClientSession() as session:
        app[session_key] = session
        yield


def make_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    app.cleanup_ctx.append(app_session)
    return app


app = make_app()
