import redis
import os


class SessionsStorage:
    uid_role: redis.Redis
    uid_data: redis.Redis
    uid_stage: redis.Redis

    def __init__(self):
        self.uid_role = redis.from_url(url=os.environ['REDISCLOUD_URL'], db=0, decode_responses=True)
        self.uid_data = redis.from_url(url=os.environ['REDISCLOUD_URL'], db=1, decode_responses=True)
        self.uid_stage = redis.from_url(url=os.environ['REDISCLOUD_URL'], db=2, decode_responses=True)

    def get_role(self, uid: int) -> str:
        print(type(self.uid_role))
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
