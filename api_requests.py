import requests
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

server_url = config["debug"]["server_url"]


def get_companies_list(uid: int) -> list:
    try:
        res = requests.post(server_url + "/companies", data={
            "telegram_id": uid,
        })

    except requests.exceptions.ConnectionError:
        return []

    res_json = res.json()
    return res_json["companies"]


def get_role(uid: int, company_guid: str) -> str:
    try:
        res = requests.post(server_url + "/role", data={
            "telegram_id": uid,
            "company": company_guid
        })

    except requests.exceptions.ConnectionError:
        return "no role"

    res_json = res.json()
    return res_json["role"]


def get_attached_workers(uid: int, company_guid: str) -> list:
    try:
        res = requests.post(server_url + "/attached_workers", data={
            "telegram_id": uid,
            "company": company_guid
        })

    except requests.exceptions.ConnectionError:
        return []

    res_json = res.json()
    return res_json["users"]


def get_workers_stats(uid: int, company_guid: str) -> list:
    try:
        res = requests.post(server_url + "/attached_workers_statistics", data={
            "telegram_id": uid,
            "company": company_guid
        })

    except requests.exceptions.ConnectionError:
        return []

    res_json = res.json()
    return res_json["users"]


def add_health_data(uid: int, company_guid: str, temp: float) -> dict():
    try:
        res = requests.post(server_url + "/add_health_data", data={
            "telegram_id": uid,
            "company": company_guid,
            "temperature": temp
        })

    except requests.exceptions.ConnectionError:
        return "False"

    res_json = res.json()
    return res_json["status"]
