import redis


class SessionsStorage:
    sessions: redis.Redis

    def __init__(self):
        self.sessions = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

    def get_role(self, uid):
        return self.sessions.get(str(uid))

    def set_role(self, uid, role):
        self.sessions.set(str(uid), str(role))

    def set_role_stage(self, uid, role, stage):
        self.sessions.set(str(uid) + '_' + str(role), str(stage))

    def get_role_stage(self, uid, role):
        return self.sessions.get(str(uid) + '_' + str(role))

    def get_data(self, uid):
        return self.sessions.get("data" + str(uid))

    def set_data(self, uid, data):
        self.sessions.set("data" + str(uid), str(data))
