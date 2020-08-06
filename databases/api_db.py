from app import db
from databases.models import User


def set_waiting_workers(guid_username_list: list):
    for worker in guid_username_list:
        worker_model = User.query.filter_by(guid=worker["guid"]).first()

        if worker_model is not None:
            worker_model.username = worker["nickname"]
        else:
            db.session.add(User(guid=worker["guid"], username=worker["nickname"]))

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


def delete_waiting_workers(guid_username_list: list):
    for worker in guid_username_list:
        worker_model = User.query.filter_by(guid=worker["guid"]).first()

        if worker_model is not None:
            db.session.delete(worker_model)

    db.session.commit()
    print("db changed (deleted)")


def confirm_deletion(username: int):
    worker = User.query.filter_by(username=username).first()
    db.session.delete(worker)
    db.session.commit()
    print("db changed (backend got id, deleted in db)")
