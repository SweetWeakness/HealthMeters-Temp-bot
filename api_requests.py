import requests
import json

from config import config_manager as cfg

server_url = cfg.get_backend_url()


def send_request(endpoint: str, data: dict) -> dict:
    body = json.dumps(data)
    headers = {
        'content-type': "application/json",
    }
    response = requests.post(server_url + endpoint, headers=headers, data=body)
    return response.json()


def get_companies_list(uid: int) -> list:
    data = {
        "telegram_id": uid,
    }
    respond_json = send_request("/companies", data)

    return respond_json["companies"]


def get_role(uid: int, company_guid: str) -> str:
    data = {
        "telegram_id": uid,
        "company": company_guid
    }
    respond_json = send_request("/role", data)

    return respond_json["role"]


def get_attached_workers(uid: int, company_guid: str) -> list:
    data = {
        "telegram_id": uid,
        "company": company_guid
    }
    respond_json = send_request("/attached_workers", data)

    return respond_json["users"]


def get_workers_stats(uid: int, company_guid: str) -> list:
    data = {
        "telegram_id": uid,
        "company": company_guid
    }
    respond_json = send_request("/attached_workers_statistics", data)

    return respond_json["users"]


def add_health_data(uid: int, company_guid: str, temp: float) -> bool:
    data = {
        "telegram_id": uid,
        "company": company_guid,
        "temperature": temp
    }
    respond_json = send_request("/add_health_data", data)

    if "status" in respond_json:
        if respond_json["status"] == "ok":
            return True

    return False


def synchronize():
    requests.get(server_url + "/synchronize")


def get_base64_file(uid: int, company_guid: str) -> str:
    data = {
        "telegram_id": uid,
        "company": company_guid,
        "type": "telegram"
    }
    respond_json = send_request("/file_statistic", data)

    return respond_json["df"]


def send_file_on_email(uid: int, company_guid: str, email: str) -> bool:
    data = {
        "telegram_id": uid,
        "company": company_guid,
        "type": "email",
        "email": email
    }
    respond_json = send_request("/file_statistic", data)

    if "status" in respond_json:
        if respond_json["status"] == "ok":
            return True

    return False
