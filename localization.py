import enum

ru = {
    "add_employee": 'Добавить сотрудника',
    "delete_employee": 'Удалить сотрудника',
    "attach_employee": 'Прикрепить сотрудника',
    "list_employee": 'Посмотреть список сотрудников',
    "stat": 'Статистика',
    "license_info": 'Статус лицензии',

    "stat_employee": 'Посмотреть статистику по сотруднику',
    "list_attach_employee": 'Вывести общую статистику',
    "common_stat": 'Вывести общую статистику',
    "ask_temp": 'Запросить измерения температуры',

    "measure_temp": 'Измерить температуру',

    "role_admin": 'Администратор',
    "role_manager": 'Менеджер',
    "role_worker": 'Сотрудник',
}

localization = {
    "ru": ru
}


class Language(enum.Enum):
    ru: str = "ru"


class Localization:
    def __init__(self, language: Language):
        self.language = language.value

    @property
    def add_employee(self) -> str:
        return localization[self.language]["add_employee"]

    @property
    def delete_employee(self) -> str:
        return localization[self.language]["delete_employee"]

    @property
    def attach_employee(self) -> str:
        return localization[self.language]["attach_employee"]

    @property
    def list_employee(self):
        return localization[self.language]["list_employee"]

    @property
    def stat(self) -> str:
        return localization[self.language]["stat"]

    @property
    def license_info(self) -> str:
        return localization[self.language]["license_info"]

    @property
    def stat_employee(self) -> str:
        return localization[self.language]["stat_employee"]

    @property
    def list_attach_employee(self) -> str:
        return localization[self.language]["list_attach_employee"]

    @property
    def common_stat(self) -> str:
        return localization[self.language]["common_stat"]

    @property
    def ask_temp(self) -> str:
        return localization[self.language]["ask_temp"]

    @property
    def measure_temp(self) -> str:
        return localization[self.language]["measure_temp"]

    @property
    def role_admin(self) -> str:
        return localization[self.language]["role_admin"]

    @property
    def role_manager(self) -> str:
        return localization[self.language]["role_manager"]

    @property
    def role_worker(self) -> str:
        return localization[self.language]["role_worker"]
