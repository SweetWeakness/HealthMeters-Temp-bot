from app import db
from app.databases.models import User


def set_waiting_workers(guid_username_list: list):
    ans = {"employees": []}
    for worker in guid_username_list:
        worker_model = User.query.filter_by(username=worker["nickname"]).first()

        if worker_model is None:
            db.session.add(User(guid=worker["guid"], username=worker["nickname"]))
        else:
            if worker_model.telegram_id is not None:
                worker_model.guid = worker["guid"]
                ans["employees"].append({worker_model.guid: worker_model.telegram_id})

    if len(ans["employees"]) == 0:
        ans = {}

    print(ans)
    db.session.commit()
    return ans


def set_worker_id(username: str, telegram_id: int):
    worker = User.query.filter_by(username=username).first()

    if worker is None:
        db.session.add(User(username=username, telegram_id=telegram_id))
        ans = {}
    else:
        if worker.telegram_id is None:
            worker.telegram_id = telegram_id
            ans = {"employees": [{worker.guid: worker.telegram_id}]}
        else:
            ans = {}

    print(ans)
    db.session.commit()
    return ans
