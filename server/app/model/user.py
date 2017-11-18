import peewee as pw
from app.model.base_model import BaseModel

class User(BaseModel):
    fb_id = pw.CharField()
    person_group = pw.CharField()