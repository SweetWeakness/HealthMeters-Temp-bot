import requests
import configparser


config = configparser.ConfigParser()
# TODO: Создать интерфейс взаимодействия с конфиг-файлом, тогда "./config.ini" вынесется в статическую
#  константу, и вся логика по получению значений из конфига будет инкапсулирована.
config.read("./config.ini")

server_url = config["release"]["server_url"]


# TODO: Стоит написать общую функцию send_request(url, data) -> json, которая делает запрос к серверу
#  и возвращает распаршеный json, а в случае ошибки - throw-ит requests.exceptions.RequestException.
def get_companies_list(uid: int) -> list:
    try:
        res = requests.post(server_url + "/companies", data={
            "telegram_id": uid,
        })

    # TODO: Ошибки стоит ловить в родительском блоке.
    except requests.exceptions.RequestException:
        return []

    res_json = res.json()
    return res_json["companies"]


def get_role(uid: int, company_guid: str) -> str:
    try:
        res = requests.post(server_url + "/role", data={
            "telegram_id": uid,
            "company": company_guid
        })

    except requests.exceptions.RequestException:
        return "no role"

    res_json = res.json()
    return res_json["role"]


def get_attached_workers(uid: int, company_guid: str) -> list:
    try:
        res = requests.post(server_url + "/attached_workers", data={
            "telegram_id": uid,
            "company": company_guid
        })

    except requests.exceptions.RequestException:
        return []

    res_json = res.json()
    return res_json["users"]


def get_workers_stats(uid: int, company_guid: str) -> list:
    try:
        res = requests.post(server_url + "/attached_workers_statistics", data={
            "telegram_id": uid,
            "company": company_guid
        })

    except requests.exceptions.RequestException:
        return []

    res_json = res.json()
    return res_json["users"]


def add_health_data(uid: int, company_guid: str, temp: float) -> bool:
    try:
        res = requests.post(server_url + "/add_health_data", data={
            "telegram_id": uid,
            "company": company_guid,
            "temperature": temp
        })

    except requests.exceptions.RequestException:
        return False

    res_json = res.json()
    if "status" in res_json:
        if res_json["status"] == "ok":
            return True

    return False
