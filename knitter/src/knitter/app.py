import logging

import aiohttp
from aiohttp import web


routes = web.RouteTableDef()
logger = logging.getLogger(__name__)

session_key = web.AppKey('session', aiohttp.ClientSession)


@routes.post("/sweater/order")
async def knit_sweater(request: web.Request) -> web.Response:

    order_data = await request.json()

    # TODO: make a call out to farmer

    return web.json_response({
        "colour": order_data["colour"],
        "order_number": order_data["order_number"],
        "style": "long_sleeved",
    })


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
