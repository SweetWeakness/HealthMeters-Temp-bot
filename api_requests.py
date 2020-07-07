import requests


server_url = 'http://127.0.0.1:8000/telegram_bot'


def get_companies_list(uid):
    res = requests.post(server_url + "/companies", data={
        "telegram_id": str(uid),
    })
    res_json = res.json()
    return res_json["companies"]


def get_role(uid, guid):
    res = requests.post(server_url + "/role", data={
        "telegram_id": str(uid),
        "company": str(guid)
    })
    res_json = res.json()
    return res_json['role']


def get_attached_workers(uid, guid):
    res = requests.post(server_url + "/attached_workers", data={
        "telegram_id": str(uid),
        "company": str(guid)
    })
    res_json = res.json()
    return res_json["users"]


def get_workers_stats(uid, guid):
    res = requests.post(server_url + "/attached_workers_statistics", data={
        "telegram_id": str(uid),
        "company": str(guid)
    })
    res_json = res.json()
    return res_json["users"]


def add_health_data(uid, guid, temp):
    res = requests.post(server_url + "/add_health_data", data={
        "telegram_id": str(uid),
        "company": str(guid),
        "temperature": temp
    })
    res_json = res.json()
    return res_json["status"]
