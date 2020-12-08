from aiohttp import web
from config.config import CONFIG

from app.handlers import basic, coder


APPLICATION = web.Application()
APPLICATION['conf'] = CONFIG


APPLICATION.add_routes([
    web.get(f'{CONFIG["api_prefix"]}/test', basic.test_connection),
    web.post(f'{CONFIG["api_prefix"]}/encode', coder.encode),
    web.post(f'{CONFIG["api_prefix"]}/decode', coder.decode)
])
