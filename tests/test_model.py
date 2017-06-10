from models import Image
from pymodm import fields


def test_url_is_urlfield():
    assert isinstance(Image.url, fields.URLField)


def test_url_is_primarykey():
    assert Image.url.primary_key


def test_small_is_imagefield():
    assert isinstance(Image.small, fields.ImageField)


def test_medium_is_imagefield():
    assert isinstance(Image.medium, fields.ImageField)


def test_large_is_imagefield():
    assert isinstance(Image.large, fields.ImageField)