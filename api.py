# coding: utf-8

import requests


BASE_API = 'https://checash.herokuapp.com/'


def create_user(**kwargs):

    r = requests.post(
        '{}{}'.format(BASE_API, 'user'),
        data={
            'first_name': kwargs.get('first_name', 'Nikita'),
            'last_name': kwargs.get('last_name', 'God'),
            'username': kwargs.get('username', 'god_nikita')
        }
    )

    json = r.json()
    return json.get('id')


def add_bill(user_id, qr):

    r = requests.post(
        '{}{}{}{}'.format(BASE_API, 'user/', user_id, '/add-bill/'),
        data=(
            {'qr': qr} if isinstance(qr, str)
            else {'fn': qr.get('fn'),
                  'i': qr.get('i'),
                  'fp': qr.get('fp'),
                  'n': qr.get('n')}
        )
    )

    return r.json()


def get_bills(user_id):

    r = requests.get(
        '{}{}{}{}'.format(BASE_API, 'user/', user_id, '/get-bills-detailed/'),
    )

    return r.json()


def get_item_info(item_id):

    r = requests.get(
        '{}{}{}{}'.format(BASE_API, 'item/', item_id, '/category')
    )

    return r.json()
