""" Translation handler module """

from .translation_client import ClientTranslateError


class ClientDoesNotExistException(Exception):
    """
    Exception triggers if client does not exist
    """


class TranslationClientHandler:
    """
    Some stuff for translation client. If we have multiple translation API's, then in case of
    fail we changing and try again.
    """
    __registered_clients = {}
    _default_client = None

    def __init__(self, clients):
        """
        Initialization.

        :param clients: list of AbstractClient childs.
        """
        for client in clients:
            self.register_client(client)

        self.set_default_client(clients[0])

    @classmethod
    def register_client(cls, client):
        """
        Add client to registered
        :param client: AbstractClient instance
        """
        cls.__registered_clients[client.client_name] = client

    @classmethod
    def set_default_client(cls, client):
        """
        Set default translation client.
        :param client: AbstractClient instance
        """
        try:
            cls._default_client = cls.__registered_clients[client.client_name]
        except KeyError:
            raise ClientDoesNotExistException(f'Client "{client.client_name}" does not exist')

    @staticmethod
    def get_registered_clients():
        """
        :return: dict data of registered items
        """
        return TranslationClientHandler.__registered_clients

    def try_translate(self, target_language, data_to_translate):
        """
        Tries to translate data to target language using default client.

        TODO: sets next client or fail
        :param target_language: Language alias, like 'en'
        :param data_to_translate: dict data, like {'name': 'Tony', 'surname': 'Ferguson'}
        :return: Translated data
        """
        try:
            return self._default_client.translate(target_language, data_to_translate)
        except ClientTranslateError:
            return {}
