import enum


ru = {
    "add_employee": "Добавить сотрудника",
    "delete_employee": "Удалить сотрудника",
    "attach_employee": "Прикрепить сотрудника",
    "list_employee": "Посмотреть список сотрудников",
    "stat": "Статистика",
    "license_info": "Статус лицензии",
    "stat_employee": "Посмотреть статистику по сотруднику",
    "list_attach_employee": "Вывести общую статистику",

    # worker buttons ----------------------------------------------------------
    "measure_temp": "Измерить температуру",

    # manager buttons ---------------------------------------------------------
    "common_stat": "Вывести общую статистику",
    "ask_measure": "Запросить измерения температуры",

    # common buttons ----------------------------------------------------------
    "mistake": "Я ошибся",
    "accept": "Все верно",
    "choose_all": "Выбрать все",

    # bot to worker phrases ---------------------------------------------------
    "insert_temp": "Введите вашу температуру (например, 36.6):",
    "ask_temp": "Ваша температура {}, все верно?",
    "temp_validation": "Мне кажется, вы где-то ошиблись. Введите вашу температуру еще раз:",
    "photo_validation": "Отправьте мне фотографию градусника:",
    "reinsert_temp": "Хорошо, введите вашу температуру еще раз:",
    "accept_temp": "Отлично, теперь отправьте мне фотографию градусника.",
    "got_photo": "Проверьте вашу фотографию (например, видна ли температура).",
    "reinsert_photo": "Тогда отправьте мне фотографию еще раз:",
    "accept_photo": "Ваша температура была записана и отправлена.",
    "accept_companies": "Я записал вашу температуру.\n"
                        "Выберите компанию, в которую нужно отправить замеры:",

    # bot to manager phrases --------------------------------------------------
    "made_stats": "Вывел общую статистику по сотрудникам.",
    "asked_measure": "Запросил измерения температуры у сотрудников.",
    "choose_company_stats": "Выберите компанию, по которой нужна статистика:",
    "choose_company_measure": "Выберите компанию, в которой нужно провести замеры:",

    # common bot phrases ------------------------------------------------------
    "greeting": "Здравствуйте!",
    "missing_reply": "Извините, я вас не понял.",
    "access_error": "У вас нет доступа. Обратитесь к администратору.",
    "manager_ask_measure": "Ваш менеджер просит измерить температуру!",
    "stats_message": "Статистика была создана автоматически",
    "system_access_error": "Вас нет в системе. Обратитесь к администратору.",

    # roles -------------------------------------------------------------------
    "role_admin": "Администратор",
    "role_manager": "Менеджер",
    "role_worker": "Сотрудник",
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

    # worker buttons ----------------------------------------------------------
    @property
    def measure_temp(self) -> str:
        return localization[self.language]["measure_temp"]

    # manager buttons ---------------------------------------------------------
    @property
    def common_stat(self) -> str:
        return localization[self.language]["common_stat"]

    @property
    def ask_measure(self) -> str:
        return localization[self.language]["ask_measure"]

    # common buttons ----------------------------------------------------------
    @property
    def mistake(self) -> str:
        return localization[self.language]["mistake"]

    @property
    def accept(self) -> str:
        return localization[self.language]["accept"]

    @property
    def choose_all(self) -> str:
        return localization[self.language]["choose_all"]

    # bot to worker phrases ---------------------------------------------------
    @property
    def insert_temp(self) -> str:
        return localization[self.language]["insert_temp"]

    @property
    def ask_temp(self) -> str:
        return localization[self.language]["ask_temp"]

    @property
    def temp_validation(self) -> str:
        return localization[self.language]["temp_validation"]

    @property
    def photo_validation(self) -> str:
        return localization[self.language]["photo_validation"]

    @property
    def reinsert_temp(self) -> str:
        return localization[self.language]["reinsert_temp"]

    @property
    def accept_temp(self) -> str:
        return localization[self.language]["accept_temp"]

    @property
    def got_photo(self) -> str:
        return localization[self.language]["got_photo"]

    @property
    def reinsert_photo(self) -> str:
        return localization[self.language]["reinsert_photo"]

    @property
    def accept_photo(self) -> str:
        return localization[self.language]["accept_photo"]

    @property
    def accept_companies(self) -> str:
        return localization[self.language]["accept_companies"]

    # bot to manager phrases --------------------------------------------------
    @property
    def made_stats(self) -> str:
        return localization[self.language]["made_stats"]

    @property
    def asked_measure(self) -> str:
        return localization[self.language]["asked_measure"]

    @property
    def choose_company_stats(self) -> str:
        return localization[self.language]["choose_company_stats"]

    @property
    def choose_company_measure(self) -> str:
        return localization[self.language]["choose_company_measure"]

    # common bot phrases ------------------------------------------------------
    @property
    def greeting(self) -> str:
        return localization[self.language]["greeting"]

    @property
    def missing_reply(self) -> str:
        return localization[self.language]["missing_reply"]

    @property
    def access_error(self) -> str:
        return localization[self.language]["access_error"]

    @property
    def manager_ask_measure(self) -> str:
        return localization[self.language]["manager_ask_measure"]

    @property
    def stats_message(self) -> str:
        return localization[self.language]["stats_message"]

    @property
    def system_access_error(self) -> str:
        return localization[self.language]["system_access_error"]

    # roles -------------------------------------------------------------------
    @property
    def role_admin(self) -> str:
        return localization[self.language]["role_admin"]

    @property
    def role_manager(self) -> str:
        return localization[self.language]["role_manager"]

    @property
    def role_worker(self) -> str:
        return localization[self.language]["role_worker"]
