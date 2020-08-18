import redis

from config import config_manager as cfg

redis_url = cfg.get_redis_url()
db_index = cfg.get_db_index()


class UserStorage:
    db: redis.Redis

    def __init__(self):
        self.db = redis.from_url(url=redis_url, db=db_index, decode_responses=True)

    # Role:

    def set_role(self, uid: int, role) -> None:
        self.db.set(str(uid), str(role))

    def get_role(self, uid: int) -> str:
        return self.db.get(str(uid))

    def role_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid))

    # Stage (bot's menu stage):

    def set_stage(self, uid: int, stage) -> None:
        self.db.set(str(uid) + "_stage", str(stage))

    def get_stage(self, uid: int) -> str:
        return self.db.get(str(uid) + "_stage")

    def stage_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid) + "_stage")

    # Data (temp/email for worker/manager):

    def set_data(self, uid: int, data: str) -> None:
        self.db.set(str(uid) + "_data", str(data))

    def get_data(self, uid: int) -> str:
        return self.db.get(str(uid) + "_data")

    def data_exist(self, uid: int) -> bool:
        return self.db.exists(str(uid) + "_data")

    def delete_data(self, uid: int) -> bool:
        return self.db.delete(str(uid) + "_data")

    # Company in context of usage:

    def set_comp_context(self, uid: int, guid: str) -> None:
        self.db.set(str(uid) + "_comp_context", str(guid))

    def get_comp_context(self, uid: int) -> str:
        return self.db.get(str(uid) + "_comp_context")

    # Language:

    def set_language(self, uid: int, lang: str) -> None:
        self.db.set(str(uid) + "_language", str(lang))

    def get_language(self, uid: int) -> str:
        return self.db.get(str(uid) + "_language")
