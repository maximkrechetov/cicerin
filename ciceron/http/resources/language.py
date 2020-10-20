"""Language resource definition and logic"""

from flask import request
from flask_restful import Resource
from pymongo.errors import DuplicateKeyError

from ciceron.helpers import to_safe_dict
from ciceron.http.validators.api_validators import RequestDataValidator, DataValidationError
from ciceron.models import Language


class LanguageResource(Resource):
    """
    HTTP resource for Language model
    """
    def get(self, id=None):
        """
        HTTP GET method
        :param id: language id
        :return: JSON data
        """
        if not id:
            return [to_safe_dict(lang) for lang in Language.objects.all()]

        try:
            request_data = RequestDataValidator(
                'get_language',
                {'id': id}
            ).validate()

            language = Language.objects.get({'_id': request_data.get('id')})

            return to_safe_dict(language)
        except Language.DoesNotExist:
            return {'errors': {'language': ['Language does not exist']}}, 404
        except DataValidationError as exc:
            return {'errors': exc.errors}, 400

    def post(self):
        """
        HTTP POST method
        :return: JSON data
        """
        try:
            request_data = RequestDataValidator('create_language', request.get_json()).validate()
            language = Language(**request_data).save()

            return to_safe_dict(language)
        except DataValidationError as exc:
            return {'errors': exc.errors}, 400
        except DuplicateKeyError:
            return {'errors': {'alias': ['Language with same alias already exists.']}}, 409

    def put(self, id):
        """
        HTTP PUT method
        :param id: language id
        :return: JSON data
        """
        editable_fields = ['alias', 'label', 'parent']

        try:
            request_data = RequestDataValidator(
                'update_language',
                {'id': id, **request.get_json()}
            ).validate()

            language = Language.objects.get({'_id': request_data.get('id')})

            for field in editable_fields:
                setattr(language, field, request_data.get(field))

            language.save()

            return to_safe_dict(language)
        except DataValidationError as exc:
            return {'errors': exc.errors}, 400
        except Language.DoesNotExist:
            return {'errors': {'language': ['Language does not exist']}}, 404
        except DuplicateKeyError:
            return {'errors': {'alias': ['Language with same alias already exists.']}}, 409

    def delete(self, id):
        """
        HTTP DELETE method
        :param id: language id
        :return: JSON data
        """
        try:
            request_data = RequestDataValidator(
                'get_language',
                {'id': id}
            ).validate()

            deleted = Language.objects.raw({'_id': request_data.get('id')}).delete()

            if deleted:
                return {'ok': True}

            return {'errors': {'id': ['Language does not exists']}}, 404
        except DataValidationError as exc:
            return {'errors': exc.errors}, 400
