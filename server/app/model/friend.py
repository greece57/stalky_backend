import peewee as pw
from app.model.base_model import BaseModel

class Friend(BaseModel):
    from app.model.user import User

    fb_id = pw.CharField()
    name = pw.CharField()
    person_id = pw.CharField()
    last_seen_location = pw.CharField()
    last_seen_date = pw.CharField()
    user = pw.ForeignKeyField(User)
