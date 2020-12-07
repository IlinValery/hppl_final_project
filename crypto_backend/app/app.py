from aiohttp import web
from config.config import CONFIG

from app.handlers import basic


APPLICATION = web.Application()
APPLICATION['conf'] = CONFIG


APPLICATION.add_routes([
    web.get(f'{CONFIG["api_prefix"]}/test', basic.test_connection)
])
