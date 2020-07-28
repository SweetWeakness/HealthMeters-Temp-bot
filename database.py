import redis
import os


# TODO: я бы переименовал в UserStorage.
class SessionsStorage:
    db: redis.Redis

    def __init__(self, state):
        if state == "release":
            redis_url = os.environ['REDISCLOUD_URL']
        else:
            # TODO: стоит вынести в конфиг.
            redis_url = "redis://localhost:6379"
        # TODO: db тоже стоит вынести в конфиг
        self.db = redis.from_url(url=redis_url, db=0, decode_responses=True)

    # Role:

    def set_role(self, uid: int, role: str) -> None:
        self.db.set(str(uid), str(role))

    def get_role(self, uid: int) -> str:
        return self.db.get(str(uid))

    def role_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid))

    # Stage:

    def set_stage(self, uid: int, stage: str) -> None:
        # TODO: пробел стоит заменить на _: " stage" -> "_stage"
        self.db.set(str(uid) + " stage", str(stage))

    def get_stage(self, uid: int) -> str:
        return self.db.get(str(uid) + " stage")

    def stage_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid) + " stage")

    # Data:

    def set_data(self, uid: int, data: str) -> None:
        # TODO: пробел стоит заменить на _: " data" -> "_data"
        self.db.set(str(uid) + " data", str(data))

    def get_data(self, uid: int) -> str:
        return self.db.get(str(uid) + " data")
