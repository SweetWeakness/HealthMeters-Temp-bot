from app import db


class User_foad_heroku(db.Model):
    date = db.Column(db.DateTime, primary_key=True)
    id = db.Column(db.Integer)
