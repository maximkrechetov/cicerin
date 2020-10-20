""" Translation admin resource definition and logic"""

from flask import request
from flask_restful import Resource

from ciceron.helpers import to_safe_dict
from ciceron.http.validators.api_validators import RequestDataValidator, DataValidationError
from ciceron.models import Language, TranslationObject, TranslationStatus


def _create_filters(request_data):
    """
    Creates filters dict
    :param request_data: dict
    :return: dict
    """
    filters = request_data.copy()

    if 'language' in filters:
        language = Language.get_by_alias(request_data.get('language'))

        if language:
            filters['language'] = language.pk
        else:
            del filters['language']

    return filters


def _get_translation_object_by_id(object_id):
    """
    Get Translation object data by given ObjectId
    :param object_id: bson.ObjectId of TranslationObject
    :return: dict
    """
    try:
        request_data = RequestDataValidator(
            'get_translation',
            {'id': object_id}
        ).validate()

        t_object = TranslationObject.objects.get({'_id': request_data.get('id')})

        return to_safe_dict(t_object)
    except TranslationObject.DoesNotExist:
        return {'errors': {'translation': ['TranslationObject does not exist']}}, 404
    except DataValidationError as exc:
        return {'errors': exc.errors}, 400


class TranslationAdminResource(Resource):
    """
    Http resource class for TranslationObject model
    """
    def get(self, id=None):
        """
        HTTP GET method
        :param id: translation object id
        :return: JSON data
        """
        if id:
            return _get_translation_object_by_id(id)

        try:
            request_data = dict(request.args)

            if not request_data:
                return [to_safe_dict(trans) for trans in TranslationObject.objects.all()]

            request_data = RequestDataValidator(
                'filter_translations',
                request_data
            ).validate()

            filters = _create_filters(request_data)
            return [to_safe_dict(trans) for trans in TranslationObject.objects.raw(filters)]
        except DataValidationError as exc:
            return {'errors': exc.errors}, 400

    def post(self):
        """
        HTTP POST method
        :return: JSON data
        """
        try:
            created_translations = []

            request_data = RequestDataValidator('add_translation', request.get_json()).validate()
            lang, objects = request_data.values()

            language = Language.get_by_alias(lang)
            if not language:
                return {'errors': {'language': ['Language does not exist']}}, 404

            for object_key, object_data in objects.items():
                translation_object = TranslationObject(
                    language=language,
                    object_key=object_key,
                    object_data=object_data,
                    status=TranslationStatus.TRANSLATED_MANUALLY.value
                ).save()

                created_translations.append(translation_object)

            return [to_safe_dict(trans) for trans in created_translations]

        except DataValidationError as exc:
            return {'errors': exc.errors}, 400
        except Exception as exc:
            return {'errors': [str(exc)]}, 500

    def put(self, id):
        """
        HTTP PUT method
        :param id: translation object id
        :return: JSON data
        """
        try:
            request_data = RequestDataValidator(
                'update_translation',
                {'id': id, **request.get_json()}
            ).validate()

            t_object = TranslationObject.objects.get({'_id': request_data.get('id')})

            t_object.object_key = request_data.get('object_key')
            t_object.object_data = request_data.get('object_data')

            language = Language.get_by_alias(request_data.get('lang'))

            if not language:
                return {'errors': {'language': ['Language does not exist']}}, 404

            t_object.save()

            return to_safe_dict(t_object)
        except TranslationObject.DoesNotExist:
            return {'errors': {'translation': ['TranslationObject does not exist']}}, 404
        except DataValidationError as exc:
            return {'errors': exc.errors}, 400

    def delete(self, id):
        """
        HTTP DELETE method
        :param id: translation object id
        :return: JSON data
        """
        try:
            request_data = RequestDataValidator(
                'get_translation',
                {'id': id}
            ).validate()

            deleted = TranslationObject.objects.raw({'_id': request_data.get('id')}).delete()

            if deleted:
                return {'ok': True}

            return {'errors': {'id': ['TranslationObject does not exists']}}, 404
        except DataValidationError as exc:
            return {'errors': exc.errors}, 400
