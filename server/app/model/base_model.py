import peewee as pw

class BaseModel(pw.Model):
    class Meta:
        from backend.db import DB
        database = DB
