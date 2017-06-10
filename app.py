from flask_cache import Cache
from PIL import Image as ImagePL
from models import Image
from pymodm import files
from io import BytesIO
import flask


app = flask.Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})


@cache.cached(timeout=360)
@app.route("/")
def index():
    images = []
    for image in Image.objects.all():
        image_name = image.url.split("/")[-1]
        image_sizes = {field:"/{}/{}".format(field, image_name)
                       for field in image._data
                       if isinstance(getattr(image, field), files.ImageFieldFile)}
        image_fields = {"url": image.url}
        image_fields.update(image_sizes)
        images.append(image_fields)
    return flask.jsonify({"images": images})


@cache.cached(timeout=360)
@app.route("/<field>/<name>", methods=['GET'])
def get_field(field, name):
    try:
        item = Image.objects.raw({"_id": {"$regex": "({})$".format(name)}}).first()
        image = ImagePL.open(getattr(item, field))
        tmp = BytesIO()
        image.save(tmp, "JPEG")
        tmp.seek(0)
        return flask.send_file(tmp, mimetype="image/jpeg")
    except:
        return flask.jsonify({"error":"404"})


if __name__ == "__main__":
    from resizephoto import store_images
    store_images()
    app.run("0.0.0.0", debug=True)
