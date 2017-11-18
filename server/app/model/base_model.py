import peewee as pw

class BaseModel(pw.Model):
    class Meta:
        from app.db import DB
        database = DB
