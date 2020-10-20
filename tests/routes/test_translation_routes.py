""" /translate routes test """

import os
import pytest
import requests

app_url = os.environ.get('APP_URL')

if not app_url:
    pytest.skip('APP_URL environment variable is not defined', allow_module_level=True)

session = requests.Session()


def test_translate_with_wrong_data():
    resp = session.post(f'http://{app_url}/translate', json={
        'lang': 'to',
        'objects': {
            'test1': {
                'test': 'Тест'
            }
        }
    })

    assert resp.status_code == 404


def test_translate():
    resp = session.post(f'http://{app_url}/translate', json={
        'lang': 'en',
        'objects': {
            'test1': {
                'test': 'Тест'
            }
        }
    })

    assert resp.status_code == 200
