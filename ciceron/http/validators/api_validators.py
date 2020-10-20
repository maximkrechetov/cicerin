""" API validator module """

import cerberus
from bson import ObjectId
from .schemas import SCHEMAS


class DataValidationError(Exception):
    """
    Custom Exception that provides validator errors as property
    """
    def __init__(self, errors):
        super().__init__()
        self.errors = errors


OBJECTID_TYPE = cerberus.TypeDefinition('objectid', (ObjectId,), ())


class ApiValidator(cerberus.Validator):
    """
    Custom Validator extending types_mapping
    """
    types_mapping = cerberus.Validator.types_mapping.copy()
    types_mapping['objectid'] = OBJECTID_TYPE


class RequestDataValidator:
    """
    Initialization.

    :param schema: schema name
    :type schema: str
    :param data: data from JSON request
    :type data: dict
    """
    def __init__(self, schema_name, request_data):
        if not schema_name or not request_data:
            raise DataValidationError({'request': ['Schema and data both required.']})

        if schema_name not in SCHEMAS:
            raise DataValidationError({'schema': [f'Validation schema "{schema_name}" not found']})

        self.__validator = ApiValidator(SCHEMAS[schema_name])
        self.data = request_data

    def validate(self):
        """
        Validation

        :return: Validated document
        """
        if not self.__validator.validate(self.data):
            raise DataValidationError(self.__validator.errors)
        return self.__validator.document
