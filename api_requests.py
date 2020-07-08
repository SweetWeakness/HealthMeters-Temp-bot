import requests

# Todo вынести в конфиг файл
server_url = 'http://127.0.0.1:8000/telegram_bot'


def get_companies_list(uid: int) -> list:
    res = requests.post(server_url + "/companies", data={
        "telegram_id": uid,
    })
    res_json = res.json()
    return res_json["companies"]


def get_role(uid: int, company_guid: str) -> str:
    res = requests.post(server_url + "/role", data={
        "telegram_id": uid,
        "company": company_guid
    })
    res_json = res.json()
    return res_json['role']


def get_attached_workers(uid: int, company_guid: str) -> list:
    res = requests.post(server_url + "/attached_workers", data={
        "telegram_id": uid,
        "company": company_guid
    })
    res_json = res.json()
    return res_json["users"]


def get_workers_stats(uid: int, company_guid: str) -> list:
    res = requests.post(server_url + "/attached_workers_statistics", data={
        "telegram_id": uid,
        "company": company_guid
    })
    res_json = res.json()
    return res_json["users"]


def add_health_data(uid: int, company_guid: str, temp: float) -> dict():
    res = requests.post(server_url + "/add_health_data", data={
        "telegram_id": uid,
        "company": company_guid,
        "temperature": temp
    })
    res_json = res.json()
    return res_json["status"]
