""" Model helpers definition """

import datetime

from bson import ObjectId
from pymodm import MongoModel


def to_safe_dict(model_instance):
    """
    Cleans data that has been created from SON.
    :param model_instance: Must be MongoModel
    :return: dict
    """
    if not isinstance(model_instance, MongoModel):
        raise TypeError('Model instance must be MongoModel or its subclass.')

    data = model_instance.to_son().to_dict()

    for key in data:
        if isinstance(data[key], ObjectId):
            data[key] = str(data[key])
        if isinstance(data[key], (datetime.date, datetime.datetime)):
            data[key] = data[key].isoformat()

    return data
