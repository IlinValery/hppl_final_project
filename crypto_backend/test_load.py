import time
import asyncio
import aiohttp
from tqdm import tqdm
import argparse

from tests import requests as r


async def main(handler, iters, method='test'):
    t0 = time.time()
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in tqdm(range(iters)):
            task = asyncio.create_task(handler(session))
            tasks.append(task)
        await asyncio.gather(*tasks)
    print(f"Spent {time.time() - t0} seconds for testing {iters} requests of method '{method}'")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--amount", type=int,
                        help="Count of requests", default=10)
    parser.add_argument("-t", "--type", type=str,
                        help="Type of called avail function: test", default='test')
    args = parser.parse_args()

    amount = args.amount
    req_type = args.type

    handler = r.test_connection
    if req_type == 'encode':
        handler = r.test_encoder
    elif req_type == 'decode':
        handler = r.test_decoder

    asyncio.run(main(handler, amount, method=req_type))
