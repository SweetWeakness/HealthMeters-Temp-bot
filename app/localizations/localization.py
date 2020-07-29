import enum

from app.localizations import russian

localization = {
    "ru_RU": russian.ru
}


class Language(enum.Enum):
    ru: str = "ru_RU"


class Localization:
    # TODO: Language стоит переименовать в Locale.
    def __init__(self, language: Language):
        self.language = language.value

    @property
    # TODO: Итак, надеюсь ты пришел сюда из views.py, если нет – посмотри сначала TODO-шки в нем.
    #  Собственно, эта функция (уже не property) принимает uid.
    #  Далее, стоит создать функицю getLocale, которая принимает uid и возвращает Locale.
    #  Получается, пишем так: localization[self.getLocale(uid)]["add_employee"].
    #  ОДНАКО, это не позволяет избежать копипасты, ведь во всех функциях
    #  (add_employee, delete_employee, итд) - ты пишешь одну строку и меняешь только последнюю константу
    #  с, собственно, названием локализуемого свойства.
    #  Тут я предлагаю создать функцию .localize, принимающую uid и property.
    #  Тогда в функциях снизу будем писать так:
    #  self.localize(uid, "add_employee")
    #  self.localize(uid, "delete_employee")
    #  итд.
    #  Это действительно поможет избежать копипасты и трудного рефакторинга в будущем.
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
