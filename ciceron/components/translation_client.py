""" Translation clients module """

import requests


class ClientInitError(Exception):
    """
    Exception triggers at initialization errors
    """


class ClientTranslateError(Exception):
    """
     Exception triggers at translation errors
    """


class AbstractClient:
    """
    Abstract API client.
    """
    client_name = 'dummy'

    def __init__(self, api_host, **kwargs):
        """
        Initialization

        :param api_host: Host of translation server
        :type api_host: str
        :param kwargs: kw-data, automatically sets to client instance props
        :type kwargs: dict
        """
        self._api_host = api_host
        self._client_session = requests.Session()

        if not self._api_host:
            raise ClientInitError('API host must not be empty.')

        for key, value in kwargs.items():
            setattr(self, f'_{key}', value)

    def translate(self, target_language, data_to_translate):
        """
        Main method, so it must be implemented.
        :param target_language: language alias
        :type target_language: str
        :param data_to_translate: dict data in format {'x': 'Value', 'y': Value}
        :return: translated data
        """
        raise NotImplementedError('Translate method must be implemented.')


class YandexClient(AbstractClient):
    """
    Client uses Yandex.Cloud, needs folder_id
    """
    client_name = 'yandex'
    _api_key = None
    _folder_id = None

    def __init__(self, api_host, **kwargs):
        super(YandexClient, self).__init__(api_host, **kwargs)

    def translate(self, target_language, data_to_translate):
        """
        Main method, goes to Yandex.Cloud V2.
        Api reference here: https://cloud.yandex.ru/docs/translate/api-ref/Translation/translate

        :param target_language: language alias
        :type target_language: str
        :param data_to_translate: dict data in format {'x': 'Value', 'y': Value}
        :return: translated data
        """
        headers = {'Authorization': f'Api-Key {self._api_key}'}

        resp = self._client_session.post(
            f'{self._api_host}/translate',
            headers=headers,
            json={
                'folder_id': self._folder_id,
                'targetLanguageCode': target_language,
                'texts': list(data_to_translate.values())
            }
        )

        if resp.status_code != 200:
            raise ClientTranslateError(f'Client responded {resp.status_code}, translation failed.')

        translations = resp.json().get('translations', [])

        if not translations:
            return {}

        translated = {}

        for index, key in enumerate(data_to_translate):
            translated[key] = translations[index].get('text', '')

        return translated
