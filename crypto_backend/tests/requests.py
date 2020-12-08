BASE_URL = 'http://0.0.0.0:5000/api'


async def test_connection(session):
    async with session.get(f'{BASE_URL}/test', allow_redirects=True, verify_ssl=False) as response:
        if response.status == 200:
            pass
            # data = await response.read()
            # print(data)
