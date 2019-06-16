import logging

from aiohttp import web

from .controllers import routes

logger = logging.getLogger('aiohttp.server')

app = web.Application()
app.add_routes(routes)
logging.basicConfig(level=logging.DEBUG)
