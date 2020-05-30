import requests


server_url = 'http://151.248.122.100:8000'

def user_have_access(uid):
    print(uid)
    res = requests.post(server_url + '/position/', data={
        'telegram_id': str(uid)
    })
    print(res.text)
    res_json = res.json()
    print(res_json)
    try:
        return res_json['position']
    except:
        return ''

def get_manager_list(uid):
    res = requests.post(server_url + '/list/', data={
        "type": "manage_list",
        "telegram_id": str(uid)
    })
    return res.json()

def get_manager_stat(uid):
    res = requests.get(server_url + '/statistic/', data={
        "type": "manage_statistics",
        "telegram_id": str(uid)
    })
    return res.json()

def add_worker_temp(uid, temp):
    res = requests.post(server_url + '/user/', data={
        "telegram_id": uid,
        "temperature": str(temp)
    })