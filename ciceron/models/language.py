""" Language model module """

from pymodm import MongoModel, fields
from pymongo.operations import IndexModel


class Language(MongoModel):
    alias = fields.CharField(required=True)
    label = fields.CharField(required=True)
    parent = fields.ObjectIdField(blank=True, default=None)

    @classmethod
    def get_all(cls):
        """
        Get list of all language aliases
        :return: ['en_us', ...]
        :rtype: list
        """
        return [lang.alias for lang in cls.objects.all()]

    @classmethod
    def get_by_alias(cls, alias):
        """
        Get Language by alias
        :param alias: alias, like 'en_us' and s.o.
        :type: string
        :return: Language instance
        :rtype: Language
        """
        if not alias:
            return None

        try:
            return cls.objects.get({'alias': alias})
        except cls.DoesNotExist:
            return None

    class Meta:
        final = True
        indexes = [
            IndexModel('alias', unique=True)
        ]
