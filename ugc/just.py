import requests

API = '78e1d0698eb0e27850348ee237c73677'


def create_order(service_id, link, quantity):
    data = {'key': API, 'action': "add", 'service': service_id, 'link': link, 'quantity': quantity}
    response = requests.post('https://justanotherpanel.com/api/v2', data=data)
    return response.json()['order']


def get_status_order(order_id):
    data = {'key': API, 'action': "status", 'order': order_id}
    response = requests.post('https://justanotherpanel.com/api/v2', data=data)
    return response.json()['status']
