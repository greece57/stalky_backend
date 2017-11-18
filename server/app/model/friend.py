import peewee as pw
from model.base_model import BaseModel

class Friend(BaseModel):
    fb_id = pw.CharField()
    name = pw.CharField()
    face_id = pw.CharField()
