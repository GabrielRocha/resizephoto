# Resize Photos – Challenge

Given a Webservice endpoint( http://54.152.221.29/images.json ), that returns a JSON of ten photos, consume it and generate three different photo formats for each one, that must be small (320x240), medium (384x288) and large (640x480).

Finally, write a Webservice endpoint, which should use a non-relational database(MongoDB preferred) and list (in JSON format) all ten photos with their respective formats, providing their URLs.

### Dev
Install Libs
```
$ pip install -r requirements.txt
```

Create Mongodb Docker Image
```
$ docker build Docker/mongodb -t mongodb
```

Run Docker
```
$ docker run -ti -p 27017:27017 mongodb
```


### Test
```
$ pytest  --cov-report term-missing --cov . -W ignore --cov-config .coveragerc
```

### Save Images From Json
To resize and save the images it is necessary to set the basic informations in the settings.py

* Address of Json => URL
* Host, Port and DataBase name => DATABASE
* Size of new images => SIZES

Run the method store_images
```python
from resizephoto import store_images
store_images()
```

