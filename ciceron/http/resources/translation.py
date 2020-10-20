"""Translation resource definition and logic"""


import datetime

from flask import request
from flask_restful import Resource

from ciceron.components import TRANSLATION_CLIENT_HANDLER as TCH
from ciceron.http.validators.api_validators import RequestDataValidator, DataValidationError
from ciceron.models import Language, TranslationObject, TranslationStatus


class TranslationResource(Resource):
    """
    HTTP-resource class to handle main service logic.
    """
    def post(self):
        """
        POST HTTP method
        :return: JSON data
        """
        try:
            request_data = RequestDataValidator('add_translation', request.get_json()).validate()

            lang = request_data.get('lang')
            force = request_data.get('force', False)

            language = Language.get_by_alias(lang)
            if not language:
                return {'errors': {'language': ['Language does not exist']}}, 404

            objects = {}

            for object_key, object_data in request_data.get('objects', {}).items():
                translation_object = TranslationObject.get_or_create(language, object_key)

                if force:
                    to_translate = object_data
                else:
                    to_translate = {
                        key: object_data[key]
                        for key in object_data.keys()
                        if key not in (translation_object.object_data or {})
                    }

                if to_translate:
                    translations = TCH.try_translate(lang, to_translate)

                    if translations:
                        translation_object.object_data.update(translations)
                        translation_object.status = TranslationStatus.TRANSLATED_AUTOMATICALLY.value
                        translation_object.updated_at = datetime.datetime.now()
                        translation_object.save()

                objects[object_key] = translation_object.object_data

            return {'lang': lang, 'objects': objects}

        except DataValidationError as exc:
            return {'errors': exc.errors}, 400
        except Exception as exc:
            return {'errors': [str(exc)]}, 500
