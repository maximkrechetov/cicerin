""" TranslationObject model module """

from datetime import datetime
from enum import Enum
from pymodm import MongoModel, fields
from .language import Language


class TranslationStatus(Enum):
    NOT_TRANSLATED = 0
    TRANSLATED_AUTOMATICALLY = 1
    TRANSLATED_MANUALLY = 2


class TranslationObject(MongoModel):
    language = fields.ReferenceField(Language, on_delete=fields.ReferenceField.CASCADE)
    object_key = fields.CharField(required=True)
    status = fields.IntegerField(default=TranslationStatus.NOT_TRANSLATED.value)
    object_data = fields.DictField(default={}, blank=True)
    created_at = fields.DateTimeField(default=datetime.now())
    updated_at = fields.DateTimeField(default=datetime.now())

    class Meta:
        final = True

    @classmethod
    def get_or_create(cls, language, object_key):
        """
        Get TranslationObject instance by language & object key.
        Creates new record if instance does not exist.

        :param language: Language instance
        :param object_key: key that represents rest json data

        :return: TranslationObject
        """
        try:
            instance = cls.objects.get({'language': language.pk, 'object_key': object_key})
        except cls.DoesNotExist:
            instance = cls(
                language=language,
                object_key=object_key,
                object_data={}
            )

        return instance
