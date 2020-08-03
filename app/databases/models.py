from app import db


class User(db.Model):
    guid = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(32), index=True)
