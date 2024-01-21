import logging
import os

from aiohttp import web
from coldperson import app


def main():
    logging.basicConfig(level=logging.INFO)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app.app, port=port)
