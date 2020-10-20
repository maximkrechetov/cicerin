""" /api routes tests """

import os
import pytest
import requests

app_url = os.environ.get('APP_URL')

if not app_url:
    pytest.skip('APP_URL environment variable is not defined', allow_module_level=True)

session = requests.Session()

""" LANGUAGES """


def test_create_language_without_alias():
    resp = session.post(f'http://{app_url}/api/language', json={'alias': None})
    assert resp.status_code == 400


def test_create_language_with_wrong_alias():
    resp = session.post(f'http://{app_url}/api/language', json={'alias': 123})
    assert resp.status_code == 400


def test_create_language_without_label():
    resp = session.post(f'http://{app_url}/api/language', json={'alias': 'fr'})
    assert resp.status_code == 400


def test_create_language_with_wrong_label():
    resp = session.post(f'http://{app_url}/api/language', json={'alias': 'fr', 'label': 123})
    assert resp.status_code == 400


def test_create_language():
    resp = session.post(f'http://{app_url}/api/language', json={'alias': 'fr', 'label': 'French'})
    assert resp.status_code == 200

    session.language_id = resp.json().get('_id')


def test_create_language_with_existing_alias():
    resp = session.post(f'http://{app_url}/api/language', json={'alias': 'fr', 'label': 'French'})
    assert resp.status_code == 409


def test_get_languages():
    resp = session.get(f'http://{app_url}/api/language')

    assert resp.status_code == 200
    assert resp.json()


def test_get_language_with_wrong_id():
    resp = session.get(f'http://{app_url}/api/language/ef4ewfefefefef')

    assert resp.status_code == 400


def test_get_language():
    resp = session.get(f'http://{app_url}/api/language/{session.language_id}')

    assert resp.status_code == 200


def test_update_language():
    resp = session.put(f'http://{app_url}/api/language/{session.language_id}', json={
        'label': 'Franzosisch',
        'alias': 'fr'
    })

    assert resp.status_code == 200


""" TRANSLATION OBJECTS """


def test_create_t_object_w_wrong_data():
    resp = session.post(f'http://{app_url}/api/translation', json={
        'lang': 'to',
        'objects': {
            'test1': {
                'test': 'test'
            }
        }
    })

    assert resp.status_code == 404


def test_create_t_object():
    resp = session.post(f'http://{app_url}/api/translation', json={
        'lang': 'fr',
        'objects': {
            'test1': {
                'test': 'test'
            }
        }
    })

    assert resp.status_code == 200

    session.t_object_id = resp.json()[0].get('_id')


def test_get_t_objects():
    resp = session.get(f'http://{app_url}/api/translation')

    assert resp.status_code == 200
    assert resp.json()


def test_get_t_objects_with_filters():
    resp = session.get(f'http://{app_url}/api/translation?language=fr')

    assert resp.status_code == 200
    assert resp.json()


def test_get_t_object():
    resp = session.get(f'http://{app_url}/api/translation/{session.t_object_id}')

    assert resp.status_code == 200


def test_get_t_object_with_wrong_id():
    resp = session.get(f'http://{app_url}/api/translation/edrtgyjukiolp')

    assert resp.status_code == 400


def test_update_t_object():
    resp = session.put(f'http://{app_url}/api/translation/{session.t_object_id}', json={
        'lang': 'fr',
        'object_key': 'test2',
        'object_data': {'test_12': 'test_12'}
    })

    assert resp.status_code == 200


def test_delete_t_object():
    resp = session.delete(f'http://{app_url}/api/translation/{session.t_object_id}')
    assert resp.status_code == 200


def test_delete_language():
    resp = session.delete(f'http://{app_url}/api/language/{session.language_id}')
    assert resp.status_code == 200
