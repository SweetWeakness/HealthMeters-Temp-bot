from app import db


class User(db.Model):
    guid = db.Column(db.String(36), index=True, unique=True)
    username = db.Column(db.String(32), primary_key=True)
    telegram_id = db.Column(db.Integer, index=True, unique=True)
