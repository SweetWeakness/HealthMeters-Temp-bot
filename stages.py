from enum import IntFlag

MAIN = 0
ONE = 1


class ManagerStage(IntFlag):
    GET_INFO = 1


class WorkerStage(IntFlag):
    GET_TEMP = 2
    VALIDATION_TEMP = 3
    ACCEPT_TEMP = 4
    GET_PHOTO = 5
    ACCEPT_PHOTO = 6


class Role(IntFlag):
    SUPER_ADMIN = 0
    ADMIN = 1
    MANAGER = 2
    WORKER = 3
