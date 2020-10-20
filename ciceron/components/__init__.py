"""Clients and translation handler inits"""

from os import environ

from .translation_client import YandexClient
from .translation_handler import TranslationClientHandler


CLIENTS = [
    YandexClient(
        api_host=environ.get('YANDEX_HOST'),
        folder_id=environ.get('YANDEX_CATALOG_ID'),
        api_key=environ.get('YANDEX_API_KEY')
    )
]

TRANSLATION_CLIENT_HANDLER = TranslationClientHandler(CLIENTS)
