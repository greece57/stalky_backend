import peewee as pw
from app.model.base_model import BaseModel

class Image(BaseModel):
    from app.model.friend import Friend

    image_fb_id = pw.CharField()
    source_url = pw.CharField()
    x = pw.DoubleField()
    y = pw.DoubleField()
    persisted_face_id = pw.CharField()
    friend = pw.ForeignKeyField(Friend)
