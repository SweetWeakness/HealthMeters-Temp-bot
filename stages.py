from enum import IntFlag


class ManagerStage(IntFlag):
    GET_LANG = 1
    CHOOSING_OPTION = 2
    MULTICOMPANY_TEXT_STATS = 3  # choosing companies for stats
    MULTICOMPANY_MEASURE = 4  # choosing companies for asking measurement
    MULTICOMPANY_FILE_STATS = 5
    MULTICOMPANY_EMAIL_STATS = 6
    GET_STAT_TYPE = 7
    ASK_MEASURE = 8
    GET_EMAIL = 9
    VALIDATION_TEMP = 10
    ACCEPT_TEMP = 11
    GET_PHOTO = 12


class WorkerStage(IntFlag):
    GET_LANG = 8
    GET_TEMP = 9
    VALIDATION_TEMP = 10
    ACCEPT_TEMP = 11
    GET_PHOTO = 12
    GET_COMPANY = 14


class Role(IntFlag):
    MANAGER = 1
    WORKER = 2
    NOBODY = 3
