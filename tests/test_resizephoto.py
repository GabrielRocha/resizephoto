from resizephoto import read_json, resize, generate_thumbnail, store_images
from settings import URL
from io import BufferedReader, BytesIO
from PIL import Image as ImagePL
from models import Image
import pytest
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def test_json_contains_key_images():
    assert "images" in read_json(URL)


def test_json_contains_urls():
    for itens in read_json(URL)['images']:
        assert "url" in itens


def test_invalid_json():
    with pytest.raises(ValueError) as error:
        read_json("http://error/error.json")
    assert "Invalid Json" == str(error.value)


@pytest.mark.parametrize("size", [("small", (320, 240)),
                                  ("medium", (384, 288)),
                                  ("large", (640, 480))])
def test_resize(size):
    with open(BASE_DIR+"/images/b737_5.jpg", "rb") as image:
        images = resize(image.read())
    tag, dimension = size
    width, height = dimension
    image = ImagePL.open(BytesIO(images[tag].read()))
    assert tag in images
    assert isinstance(images[tag], BufferedReader)
    assert image.width == width
    assert image.height == height


@pytest.mark.asyncio
async def test_generate(clear):
    await generate_thumbnail("http://54.152.221.29/images/b737_5.jpg")
    assert Image.objects.count() == 1
    assert Image.objects.first().url == "http://54.152.221.29/images/b737_5.jpg"


@pytest.mark.asyncio
@pytest.mark.parametrize("size", ["small", "medium", "large"])
async def test_image_in_db(size, clear):
    await generate_thumbnail("http://54.152.221.29/images/b737_5.jpg")
    assert Image.objects.count() == 1
    image = ImagePL.open(BASE_DIR+"/images/{}.jpg".format(size))
    assert getattr(Image.objects.first(), size).image.tobytes() == image.tobytes()


def test_store_images(clear):
    store_images()
    assert Image.objects.count() == 10
