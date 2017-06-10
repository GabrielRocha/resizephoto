from resizephoto import generate_thumbnail
from PIL import Image as ImagePL
import app as flask_app
import pytest
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def app():
    return flask_app.app


def test_status_code_index(client):
    assert client.get("/").status_code == 200


@pytest.mark.asyncio
async def test_status_code_index(client, clear):
    await generate_thumbnail("http://54.152.221.29/images/b737_5.jpg")
    json = client.get("/").json['images'][0]
    assert "b737_5.jpg" in json['url']
    assert "/small/b737_5.jpg" in json['small']
    assert "/medium/b737_5.jpg" in json['medium']
    assert "/large/b737_5.jpg" in json['large']


@pytest.mark.asyncio
async def test_get_image(client, clear):
    await generate_thumbnail("http://54.152.221.29/images/b737_5.jpg")
    image = ImagePL.open(client.get("/small/b737_5.jpg"))
    image_test = ImagePL.open(BASE_DIR+"/images/small.jpg")
    assert getattr(image.tobytes() == image_test.tobytes())