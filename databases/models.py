from app import db


class User(db.Model):
    picture = db.Column(db.LargeBinary)
    num = db.Column(db.Integer, primary_key=True)
    len = db.Column(db.Integer)

