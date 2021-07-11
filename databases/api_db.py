from app import db
from databases.models import User_foad_heroku as User
from sqlalchemy import func
import datetime
from databases.users import voc, users


def first_commit():
    User.query.delete()
    dt_now = datetime.datetime.today()
    dlt = datetime.timedelta(seconds=1)
    for user in users:
        db.session.add(User(date=dt_now, id=user))
        dt_now += dlt
    db.session.commit()


def add_note(user_id, amount):
    user_garbage = User.query.filter_by(id=user_id).order_by(User.date.desc()).first()
    dt_now = datetime.datetime.today()
    if user_garbage is not None:
        if user_garbage.date + datetime.timedelta(seconds=10) > dt_now:
            return "Больной нахуй, 2 минуты еще не прошло" + str(user_garbage.date) + " " + str(datetime.timedelta(seconds=10) + " " + str(dt_now)

    db.session.add(User(date=dt_now, id=user_id))
    if amount == 2:
        db.session.add(User(date=dt_now + datetime.timedelta(seconds=1), id=user_id))

    db.session.commit()
    print("db changed (added)")

    return "Добавил твой отчет в бд, имеем:"


def get_stats(user_id):
    stats = User.query.with_entities(User.id, func.count(User.id)).group_by(User.id).all()
    stats = [list(stat) for stat in stats]
    stats = sorted(stats, key=lambda x: x[1], reverse=True)

    exit_code = [""]
    for stat in stats:
        if stats[0][1] - stat[1] > 3:
            exit_code.append(stat[0])

        if stat[0] == user_id:
            exit_code[0] += "(Ты)👉 "
        exit_code[0] += ("%s: %s\n" % (voc[stat[0]], stat[1] - 1))

    return exit_code

