import aiohttp
from aiohttp import FormData

BASE_URL = 'http://0.0.0.0:5000/api'

from tests.constants import image_str_origin, encoded_image, key, text


async def test_connection(session):
    async with session.get(f'{BASE_URL}/test', allow_redirects=True, verify_ssl=False) as response:
        if response.status == 200:
            pass
            # data = await response.read()
            # print(data)


async def test_encoder(session):
    data = FormData()

    data.add_field('image', image_str_origin, content_type='text/plain')
    data.add_field('text', text, content_type='text/plain')
    data.add_field('key', key, content_type='text/plain')
    async with session.post(f'{BASE_URL}/encode', data=data) as response:
        if response.status == 200:
            # data = await response.read()
            # print(data)
            pass
        else:
            print(response.status)


async def test_decoder(session):
    data = FormData()
    data.add_field('image', encoded_image, content_type='text/plain')
    data.add_field('key', key, content_type='text/plain')
    async with session.post(f'{BASE_URL}/decode', data=data) as response:
        if response.status == 200:
            # data = await response.read()
            # print(data)
            pass
        else:
            print(response.status)
