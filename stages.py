from enum import Enum

MAIN = 0

class AddEmployeeStage(Enum):
    GET_NAME = 1
    GET_USERNAME = 2
    GET_POSITION = 3
    USER_ADDED = 4

class DeleteEmployeeStage(Enum):
    GET_USERNAME = 5

class AttachEmployeeStage(Enum):
    GET_MANAGER_USERNAME = 6
    GET_USERNAME = 7

class StatEmployeeStage(Enum):
    GET_USERNAME = 8

class MeasureTempStage(Enum):
    GET_TEMP = 9
    GET_PHOTO = 10

class Role(Enum):
    SUPER_ADMIN = 0
    ADMIN = 1
    MANAGER = 2
    WORKER = 3