import logging

from aiohttp import web

from .controllers import routes
from .database import connection

logger = logging.getLogger('aiohttp.server')


async def on_start(app: web.Application):
    await connection()

app = web.Application()

logging.basicConfig(level=logging.DEBUG)
app.add_routes(routes)
app.on_startup.append(on_start)

