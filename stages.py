from enum import IntFlag


class ManagerStage(IntFlag):
    GET_LANG = 1
    CHOOSING_OPTION = 2
    MULTICOMPANY_STATS = 3  # choosing companies for stats
    MULTICOMPANY_MEASURE = 4  # choosing companies for asking measurement
    GET_STAT_TYPE = 5
    ASK_MEASURE = 6
    GET_EMAIL = 7


class WorkerStage(IntFlag):
    GET_LANG = 8
    GET_TEMP = 9
    VALIDATION_TEMP = 10
    ACCEPT_TEMP = 11
    GET_PHOTO = 12
    ACCEPT_PHOTO = 13
    GET_COMPANY = 14


class Role(IntFlag):
    MANAGER = 1
    WORKER = 2
    NOBODY = 3
