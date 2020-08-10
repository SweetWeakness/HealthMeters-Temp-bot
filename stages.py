from enum import IntFlag


class ManagerStage(IntFlag):
    CHOOSING_OPTION = 1
    GET_INFO = 2  # choosing companies for stats
    ASK_TEMP = 3  # choosing companies for asking measurement
    GET_STAT = 4
    ASK_MEASURE = 5
    GET_EMAIL = 6


class WorkerStage(IntFlag):
    GET_TEMP = 4
    VALIDATION_TEMP = 5
    ACCEPT_TEMP = 6
    GET_PHOTO = 7
    ACCEPT_PHOTO = 8
    GET_COMPANY = 9


class Role(IntFlag):
    MANAGER = 1
    WORKER = 2
    NOBODY = 3
