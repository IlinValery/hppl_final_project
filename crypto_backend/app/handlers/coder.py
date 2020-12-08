import aiohttp
from aiohttp import web
import numpy as np
import base64
from PIL import Image
import io
import random

from aiohttp.abc import Request


def get_seed(key: str):
    key_seed = 1
    key = key.lower()
    for i in range(len(key) - 1):
        key_seed *= ord(key[i]) * (ord(key[i]) - ord(key[i + 1]))
    return key_seed


async def transform_base64_to_np_image(base64str: str):
    decoded_image = base64.b64decode(base64str)
    image = Image.open(io.BytesIO(decoded_image))
    return np.array(image)


async def transform_np_image_to_base64(array: np.ndarray):
    img = Image.fromarray(array)
    im_file = io.BytesIO()
    img.save(im_file, format="BMP")
    im_bytes = im_file.getvalue()
    return f'data:image/bmp;base64,{base64.b64encode(im_bytes).decode("utf-8")}'


async def encode(request: Request):
    image = None
    key = None
    text = None
    async for field in (await request.multipart()):
        if field.name == 'image':
            image = (await field.read()).decode().split(',')[1]
        if field.name == 'key':
            key = (await field.read()).decode()
        if field.name == 'text':
            text = (await field.read()).decode()
    if not (image and key and text):
        return web.Response(text="No required keys found", status=500)

    image = await transform_base64_to_np_image(image)

    img_size = image.shape[0] * image.shape[1]
    text_size = len(text)
    if text_size == 0:
        return web.Response(text="Empty text file", status=500)
    elif text_size > img_size:
        return web.Response(text="Image is too small", status=500)
    text += '\0'
    text_size += 1

    generator = random.Random()
    generator.seed(get_seed(key))

    wpixs = []
    for i in range(text_size):
        while True:
            ix = generator.randint(0, image.shape[0] - 1)
            iy = generator.randint(0, image.shape[1] - 1)
            if (ix, iy) not in wpixs:
                wpixs.append((ix, iy))
                break
        this_char = ord(text[i])
        if this_char > 1000:
            this_char -= 890  # for russian letters
        #  rgb converting
        image[ix, iy, 0] = (image[ix, iy, 0] & (0x1F << 3)) | ((this_char & 0xE0) >> 5)
        image[ix, iy, 1] = (image[ix, iy, 1] & (0x3F << 2)) | ((this_char & 0x18) >> 3)
        image[ix, iy, 2] = (image[ix, iy, 2] & (0x1F << 3)) | (this_char & 0x7)

    return web.json_response({"image": await transform_np_image_to_base64(image)}, status=200)


async def decode(request):
    image = None
    key = None
    async for field in (await request.multipart()):
        if field.name == 'image':
            image = (await field.read()).decode().split(',')[1]
        if field.name == 'key':
            key = (await field.read()).decode()

    if not (image and key):
        return web.Response(text="No required keys found", status=500)

    image = await transform_base64_to_np_image(image)

    generator = random.Random()
    generator.seed(get_seed(key))

    decrypt_text = ""

    wpixs = []
    while True:
        while True:
            ix = generator.randint(0, image.shape[0] - 1)
            iy = generator.randint(0, image.shape[1] - 1)
            if (ix, iy) not in wpixs:
                wpixs.append((ix, iy))
                break
        thisChar = 0
        thisChar |= ((image[ix, iy, 0] & 0x7) << 5)
        thisChar |= ((image[ix, iy, 1] & 0x3) << 3)
        thisChar |= (image[ix, iy, 2] & 0x7)

        if thisChar > 130:
            thisChar += 890
        if thisChar == 0:
            break
        decrypt_text += chr(thisChar)
        if len(decrypt_text) > 3e3:
            print('Not correct key')
            return web.json_response(data={'error': 'Not correct key'}, status=500)

    return web.json_response({"text": decrypt_text}, status=200)
