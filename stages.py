from enum import IntFlag


class ManagerStage(IntFlag):
    GET_LANG = 0
    CHOOSING_OPTION = 1
    MULTICOMPANY_STATS = 2  # choosing companies for stats
    MULTICOMPANY_MEASURE = 3  # choosing companies for asking measurement
    GET_STAT_TYPE = 4
    ASK_MEASURE = 5
    GET_EMAIL = 6


class WorkerStage(IntFlag):
    GET_LANG = 0
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
