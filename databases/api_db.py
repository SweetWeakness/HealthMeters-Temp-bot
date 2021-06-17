from app import db
from databases.models import User
import datetime


def first_commit():
    User.query.delete()
    db.session.commit()


def add_photo(pic_bytes):
    db.session.add(User(date=datetime.datetime.today(), picture=pic_bytes))
    db.session.commit()
    print("db changed (added)")


def get_photos(amount):
    users = User.query.order_by(User.date).all()
    if amount > len(users):
        amount = len(users)

    ans = [user.picture for user in users]

    return reversed(ans[len(ans) - amount:])
