import time

import requests
import secrets

SECRET_KEY = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjBwenl6ci0wMCIsInVzZXJfaWQiOiIzODA2NzYzMzMzMzIiLCJzZWNyZXQiOiIzYmJiOWMyMmEzMjM3ZGZlMDI2M2UxZjQ2NGMzMzRmNTJhYjc0ZjU4MDU1MGRlY2Y0NWNiMDY3MThmN2YyNzQxIn19'
PUBLIC_KEY = '48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iP3g8tCsKjfYLEbGhjRtjYcXKUuPqC7etDBpMcNnPcey4W3gUx6LZYxeYnMRXszYqLE7aHczsi8ToK8guUsaPknHhw3aeVqKRwJRHQXVaTT'


def create_pay(amount: int):
    build = secrets.token_hex(8)
    data = {
       "amount": {
         "currency": "RUB",
         "value": str(amount)
       },
       "comment": "Полнение баланса",
       "expirationDateTime": "2025-12-10T09:02:00+03:00",
       "customer": {
         "phone": "78710009999",
         "email": "test@tester.com",
         "account": "454678"
       },
       "customFields" : {
         "paySourcesFilter":"qw, card",
         "themeCode": "Yvan-YKaSh",
         "yourParam1": "64728940",
         "yourParam2": "order 678"
       }
     }

    s7 = requests.Session()
    s7.headers['Accept'] = 'application/json'
    s7.headers['Content-Type'] = 'application/json'
    s7.headers['authorization'] = 'Bearer ' + SECRET_KEY

    response = s7.put(f'https://api.qiwi.com/partner/bill/v1/bills/{build}', json=data)
    link = response.text.split('payUrl":"')[1].strip('"}')
    return {'link': link, "build": build}


def check_pay(build: str):
    s7 = requests.Session()
    s7.headers['Accept'] = 'application/json'
    s7.headers['Content-Type'] = 'application/json'
    s7.headers['authorization'] = 'Bearer ' + SECRET_KEY

    response = s7.get(f'https://api.qiwi.com/partner/bill/v1/bills/{build}')
    result = response.text.split('"status":{"value":"')[1].split('","')[0]
    if result == 'PAID':
        return True
    else:
        return False


# Тест
# pay = create_pay(2)
# print(pay['link'])
# while True:
#     if check_pay('74a6bcb937c3424d'):
#         print('Платёж получен')
#         break
#     time.sleep(20)
