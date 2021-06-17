from app import db


class User(db.Model):
    date = db.Column(db.DateTime, primary_key=True)
    picture = db.Column(db.LargeBinary)
