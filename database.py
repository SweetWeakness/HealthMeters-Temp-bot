import redis


class SessionsStorage:
    uid_role: redis.Redis
    uid_data: redis.Redis
    uid_stage: redis.Redis

    def __init__(self):
        self.uid_role = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)
        self.uid_data = redis.Redis(host="127.0.0.1", port=6379, db=1, decode_responses=True)
        self.uid_stage = redis.Redis(host="127.0.0.1", port=6379, db=2, decode_responses=True)

    def get_role(self, uid: int) -> str:
        return self.uid_role.get(str(uid))

    def set_role(self, uid: int, role: str) -> None:
        self.uid_role.set(str(uid), str(role))

    def set_stage(self, uid: int, stage: str) -> None:
        self.uid_stage.set(str(uid), str(stage))

    def get_stage(self, uid: int) -> str:
        return self.uid_stage.get(str(uid))

    def get_data(self, uid: int) -> str:
        return self.uid_data.get(str(uid))

    def set_data(self, uid: int, data: str) -> None:
        self.uid_data.set(str(uid), str(data))

    def exist(self, uid: int) -> bool:
        return self.uid_role.exists(uid)
