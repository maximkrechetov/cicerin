""" Models init module """

from os import environ
from pymodm import connect

from .language import Language
from .translation_object import TranslationObject, TranslationStatus


def connect_db():
    """
    Connects to MongoDB.
    :return:
    """
    host = environ.get('CICERON_DB_HOST', 'localhost')
    port = int(environ.get('CICERON_DB_PORT', 27017))
    db = environ.get('CICERON_DB_NAME', None)
    auth_source = environ.get('CICERON_AUTH_SOURCE', 'admin')

    connect(
        f'mongodb://{host}:{port}{"/" + db if db else ""}',
        username=environ.get('CICERON_DB_USERNAME'),
        password=environ.get('CICERON_DB_PASSWORD'),
        authSource=auth_source
    )
