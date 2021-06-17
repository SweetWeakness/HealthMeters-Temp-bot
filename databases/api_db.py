from app import db
from databases.models import User


def first_commit():
    User.query.delete()
    db.session.add(User(num=0, len=0))
    db.session.commit()


def add_photo(pic_bytes):
    meta_info = User.query.filter_by(num=0).first()
    meta_info.len += 1

    db.session.add(User(num=meta_info.len, picture=pic_bytes))
    db.session.commit()
    print("db changed (added)")


def get_photo(p_num):
    meta_info = User.query.filter_by(num=0).first()
    if p_num <= meta_info.len:
        user_model = User.query.filter_by(num=meta_info.len - p_num + 1).first()
        return user_model.picture
    else:
        return -1
