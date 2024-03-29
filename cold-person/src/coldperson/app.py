import logging

import aiohttp
from aiohttp import web

from coldperson.hatter import Hatter
from coldperson.knitter import Knitter, SweaterOrder

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)

session_key = web.AppKey('session', aiohttp.ClientSession)


@routes.post("/bff/order")
async def place_order(request: web.Request) -> web.Response:

    try:
        body = await request.json()
        order = SweaterOrder.from_dict(body)
    except Exception as e:
        logger.warning('Bad request: %s', e)
        body = {'error': '???'}
        return web.json_response(body, status=400)

    knitter = Knitter(request.app[session_key])
    sweater = await knitter.get_sweater(order)

    return web.json_response(data=sweater.to_dict())


@routes.post("/bff/order/hat")
async def place_order_for_hat(request: web.Request) -> web.Response:

    order = await request.json()

    hatter = Hatter(request.app[session_key])
    hat = await hatter.get_hat(order)

    return web.json_response(hat.to_dict())


@routes.get("/healthz")
async def healthz(_: web.Request) -> web.Response:
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
