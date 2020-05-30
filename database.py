import redis


def connect():
    return redis.Redis(host='', port='', df='', password='')

def get_stage(uid):
    r = connect()

    return r.get(str(uid))

def set_stage(uid, stage):
    r = connect()

    r.set(str(uid), str(stage))

def set_stage_data(uid, stage, data):
    r = connect()

    r.set(str(uid) + '_' + str(stage), str(data))

def get_stage_data(uid, stage)
    r = connect()

    return r.get(str(uid) + '_' + str(stage))