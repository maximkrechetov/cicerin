""" /health routes """
import os
import pytest
import requests


app_url = os.environ.get('APP_URL')

if not app_url:
    pytest.skip('APP_URL environment variable is not defined', allow_module_level=True)


def test_health():
    resp = requests.get(f'http://{app_url}/health')
    assert resp.status_code == 200
