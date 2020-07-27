from enum import IntFlag


class ManagerStage(IntFlag):
    CHOOSING_OPTION = 1
    GET_INFO = 2
    ASK_TEMP = 3


class WorkerStage(IntFlag):
    GET_TEMP = 4
    VALIDATION_TEMP = 5
    ACCEPT_TEMP = 6
    GET_PHOTO = 7
    ACCEPT_PHOTO = 8
    GET_COMPANY = 9


class Role(IntFlag):
    MANAGER = 2
    WORKER = 3
    NOBODY = 4
