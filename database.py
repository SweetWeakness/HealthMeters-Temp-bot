import redis


class SessionsStorage:
    uid_role: redis.Redis
    uid_data: redis.Redis

    def __init__(self):
        self.uid_role = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
        self.uid_data = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)

    def get_role(self, uid):
        return self.uid_role.get(str(uid))

    def set_role(self, uid, role):
        self.uid_role.set(str(uid), str(role))

    def set_role_stage(self, uid, role, stage):
        self.uid_role.set(str(uid) + '_' + str(role), str(stage))

    def get_role_stage(self, uid, role):
        return self.uid_role.get(str(uid) + '_' + str(role))

    def get_data(self, uid):
        return self.uid_data.get(str(uid))

    def set_data(self, uid, data):
        self.uid_data.set(str(uid), str(data))
