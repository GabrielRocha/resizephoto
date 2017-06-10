from urllib.request import urlopen
from io import BytesIO
from PIL import Image as ImagePL
from copy import copy
from settings import SIZES, URL
from models import Image
import aiohttp
import tempfile
import json
import asyncio


def read_json(url):
    try:
        return json.loads(urlopen(url).read().decode("utf-8"))
    except:
        raise ValueError("Invalid Json")


def store_images():
    loop = asyncio.get_event_loop()
    json_images = read_json(URL)
    tasks = [asyncio.ensure_future(generate_thumbnail(image['url']))
             for image in json_images.get('images', [])]
    wait = asyncio.wait(tasks)
    result, _ = loop.run_until_complete(wait)
    loop.close()


def resize(raw_image):
    image = ImagePL.open(BytesIO(raw_image))
    images = {}
    for size, dimension in SIZES:
        handle, filepath = tempfile.mkstemp()
        thumbnail_image = copy(image)
        thumbnail_image.thumbnail(dimension)
        thumbnail_image.save(filepath, "png")
        images[size] = open(filepath, "rb")
    return images


async def generate_thumbnail(url):
    async with aiohttp.request('GET', url) as response:
        raw_image = await response.read()
    images = resize(raw_image)
    Image(url=url, **images).save()


if __name__ == "__main__":
    store_images()
