from settings import DATABASE_TEST as DATABASE
from pymodm import connect
from models import Image
import pytest

connect('mongodb://{}:{}/{}'.format(DATABASE['host'],
                                    DATABASE['port'],
                                    DATABASE['name']))


@pytest.fixture
def clear():
    Image.objects.delete()
