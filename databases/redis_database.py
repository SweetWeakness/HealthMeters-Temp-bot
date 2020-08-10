import redis
from datetime import datetime

from config import config_manager as cfg

redis_url = cfg.get_redis_url()
db_index = cfg.get_db_index()


class UserStorage:
    db: redis.Redis

    def __init__(self):
        self.db = redis.from_url(url=redis_url, db=db_index, decode_responses=True)

    # Role:

    def set_role(self, uid: int, role: str) -> None:
        self.db.set(str(uid), str(role))

    def get_role(self, uid: int) -> str:
        return self.db.get(str(uid))

    def role_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid))

    # Stage:

    def set_stage(self, uid: int, stage: str) -> None:
        self.db.set(str(uid) + "_stage", str(stage))

    def get_stage(self, uid: int) -> str:
        return self.db.get(str(uid) + "_stage")

    def stage_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid) + "_stage")

    # Data:

    def set_data(self, uid: int, data: str) -> None:
        self.db.set(str(uid) + "_data", str(data))

    def get_data(self, uid: int) -> str:
        return self.db.get(str(uid) + "_data")

    def data_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid) + "_data")

    # Date of last measuring:

    def set_last_date(self, uid: int) -> None:
        current_date = datetime.today().strftime("%d.%m")
        self.db.set(str(uid) + "_last_date", str(current_date))

    def get_last_date(self, uid: int) -> str:
        return self.db.get(str(uid) + "_last_date")
