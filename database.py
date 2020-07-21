import redis
import os


class SessionsStorage:
    db: redis.Redis

    def __init__(self, state):
        if state == "release":
            redis_url = os.environ['REDISCLOUD_URL']
            print(redis_url)
        else:
            redis_url = "redis://localhost:6379"
        self.db = redis.from_url(url=redis_url, db=0, decode_responses=True)


    def get_role(self, uid: int) -> str:
        return self.db.get(str(uid))

    def set_role(self, uid: int, role: str) -> None:
        self.db.set(str(uid), str(role))

    def set_stage(self, uid: int, stage: str) -> None:
        self.db.set(str(uid) + " stage", str(stage))

    def get_stage(self, uid: int) -> str:
        return self.db.get(str(uid) + " stage")

    def get_data(self, uid: int) -> str:
        return self.db.get(str(uid) + " data")

    def set_data(self, uid: int, data: str) -> None:
        self.db.set(str(uid) + " data", str(data))

    def role_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid))

    def stage_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid) + " stage")
