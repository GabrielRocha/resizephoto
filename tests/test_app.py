from resizephoto import generate_thumbnail
from PIL import Image as ImagePL, ImageStat, ImageOps, ImageChops
from io import BytesIO
import app as flask_app
import pytest
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def app():
    return flask_app.app


@pytest.mark.asyncio
async def test_status_code_index(client, clear):
    await generate_thumbnail("http://54.152.221.29/images/b737_5.jpg")
    json = client.get("/").json['images'][0]
    assert client.get("/").status_code == 200
    assert "b737_5.jpg" in json['url']
    assert "/small/b737_5.jpg" in json['small']
    assert "/medium/b737_5.jpg" in json['medium']
    assert "/large/b737_5.jpg" in json['large']


@pytest.mark.asyncio
async def test_get_image(client, clear):
    await generate_thumbnail("http://54.152.221.29/images/b737_5.jpg")
    image = ImagePL.open(BytesIO(client.get("/small/b737_5.jpg").data))
    image_test = ImagePL.open(BASE_DIR+"/images/small.jpg")
    diff_image = ImageChops.difference(ImageOps.grayscale(image), ImageOps.grayscale(image_test))
    # Median pixel level for each band in the image
    assert ImageStat.Stat(diff_image.histogram()).median[0] == 1


def test_invalid_json(client):
    assert client.get("/small/asdf").json['error'] == "404"