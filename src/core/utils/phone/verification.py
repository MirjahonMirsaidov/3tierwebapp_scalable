import requests
from environ import Env

env = Env(DEBUG=(bool, False))
Env.read_env()

ESKIZ_EMAIL = env('ESKIZ_EMAIL', str, "Tezishbor@gmail.com")
ESKIZ_PASSWORD = env('ESKIZ_PASSWORD', str, "YvJkZQ6zpKPWwEgfot7om3ZAqTrQ4FBNFqkOkRl1")
ESKIZ_URL = "https://notify.eskiz.uz/api/"


def get_token():
    url = ESKIZ_URL + 'auth/login'
    body = {'email': ESKIZ_EMAIL, 'password': ESKIZ_PASSWORD}
    res = requests.post(url, json=body)
    if res.status_code == 200:
        return res.json().get('data').get('token')


def send_sms(body):
    url = ESKIZ_URL + "message/sms/send"
    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.post(url, headers=headers, json=body)
    if res.status_code == 200:
        return 'success'


def send_sms_verification(phone, code):
    message = code + ' - Ваш код подтверждения от Tez ish bor'
    body = {'mobile_phone': phone, 'message': message, 'from': 4546}
    return send_sms(body)

