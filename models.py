from settings import DATABASE
from pymodm import connect, fields, MongoModel
from pymongo.write_concern import WriteConcern


connect('mongodb://{}:{}/{}'.format(DATABASE['host'],
                                    DATABASE['port'],
                                    DATABASE['name']))


class Image(MongoModel):

    url = fields.URLField(primary_key=True)
    small = fields.ImageField()
    medium = fields.ImageField()
    large = fields.ImageField()

    class Meta:
        connection_alias = 'default'
        write_concern = WriteConcern(j=True)
