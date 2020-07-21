import redis
import os


class SessionsStorage:
    uid_role: redis.Redis
    uid_data: redis.Redis
    uid_stage: redis.Redis

    def __init__(self, state):
        if state == "release":
            redis_url = os.environ['REDISCLOUD_URL']
        else:
            redis_url = "redis://localhost:6379"
        self.uid_role = redis.from_url(url=redis_url, db=0, decode_responses=True)
        self.uid_stage = redis.from_url(url=redis_url, db=1, decode_responses=True)

    def get_role(self, uid: int) -> str:
        return self.uid_role.get(str(uid))

    def set_role(self, uid: int, role: str) -> None:
        self.uid_role.set(str(uid), str(role))

    def set_stage(self, uid: int, stage: str) -> None:
        self.uid_stage.set(str(uid), str(stage))

    def get_stage(self, uid: int) -> str:
        return self.uid_stage.get(str(uid))

    def get_role_data(self, uid: int, role: str) -> str:
        return self.uid_stage.get(str(uid) + str(role))

    def set_role_data(self, uid: int, role: str, data: str) -> None:
        self.uid_stage.set(str(uid) + str(role), str(data))

    def role_exist(self, uid: int) -> bool:
        return self.uid_role.exists(uid)

    def stage_exist(self, uid: int) -> bool:
        return self.uid_stage.exists(uid)
