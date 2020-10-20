""" /docs tests """

import os
import pytest
import requests

app_url = os.environ.get('APP_URL')

if not app_url:
    pytest.skip('APP_URL environment variable is not defined', allow_module_level=True)


def test_docs_ui():
    resp = requests.get(f'http://{app_url}/docs/')

    assert resp.status_code == 200
    assert 'text/html' in resp.headers['Content-Type']


def test_internal_json():
    resp = requests.get(f'http://{app_url}/docs/api.json')

    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'application/json'
