import peewee as pw
from model.base_model import BaseModel

class Image(BaseModel):
    image_fb_id = pw.CharField()
    source_url = pw.CharField()
    x = pw.Double()
    y = pw.Double()
