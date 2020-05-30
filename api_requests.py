import requests


server_url = '151.248.122.100:8000'

def user_have_access(uid):
    print(uid)
    res = requests.get(server_url + '/position', data={
        'telegram_id': uid
    })
    res_json = res.json()
    try:
        return res_json['position']
    except:
        return ''

def get_manager_list(uid):
    res = requests.get(server_url + '/list', data={
        'telegram_id': uid
    })
    return res.json()

def get_manager_stat(uid):
    res = requests.get(server_url + '/statistic', data={
        "type": "manage_statistics",
        "telegram_id": uid
    })
    return res.json()

def add_worker_temp(uid, temp):
    res = requests.post(server_url + '/user', data={
        "telegram_id": uid,
        "temperature": str(temp)
    })