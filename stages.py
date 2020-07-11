from enum import IntFlag

MAIN = 0
ONE = 1


class ManagerStage(IntFlag):
    CHOOSING_OPTION = 1


class WorkerStage(IntFlag):
    GET_TEMP = 4
    VALIDATION_TEMP = 5
    ACCEPT_TEMP = 6
    GET_PHOTO = 7
    ACCEPT_PHOTO = 8
    GET_COMPANY = 9


class Role(IntFlag):
    SUPER_ADMIN = 0
    ADMIN = 1
    MANAGER = 2
    WORKER = 3
    NOBODY = 4
