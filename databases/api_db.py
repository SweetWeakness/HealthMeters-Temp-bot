from app import db
from databases.models import User


def add_pending_users(users_list: list):
    for user in users_list:
        user_model = User.query.filter_by(guid=user["guid"]).first()

        if user_model is not None:
            user_model.username = user["nickname"]
        else:
            db.session.add(User(guid=user["guid"], username=user["nickname"]))

    db.session.commit()
    print("db changed (added)")


def set_worker_id(username: str, telegram_id: int):
    worker = User.query.filter_by(username=username).first()

    if worker is not None:
        ans = {"employees": {worker.guid: telegram_id}}
    else:
        ans = {}

    print("db changed (found tg_id)")
    db.session.commit()
    return ans


def delete_waiting_user(user):
    user_model = User.query.filter_by(guid=user["guid"]).first()

    if user_model is not None:
        db.session.delete(user_model)

    db.session.commit()
    print("db changed (deleted tg_id %s)" % user["telegram_id"])


def confirm_deletion(username: int):
    worker = User.query.filter_by(username=username).first()
    db.session.delete(worker)
    db.session.commit()
    print("db changed (backend got id, deleted in db)")
