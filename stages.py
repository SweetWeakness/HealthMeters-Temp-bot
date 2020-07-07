from enum import Enum

MAIN = 0


class ManagerStage(Enum):
    GET_INFO = 1


class WorkerStage(Enum):
    GET_TEMP = 2
    ACCEPT_TEMP = 3
    VALIDATION_TEMP = 4
    GET_PHOTO = 5
    ACCEPT_PHOTO = 6


class Role(Enum):
    SUPER_ADMIN = 0
    ADMIN = 1
    MANAGER = 2
    WORKER = 3
