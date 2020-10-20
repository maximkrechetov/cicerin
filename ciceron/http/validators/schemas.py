""" Validation schemas config """

from bson import ObjectId

SCHEMAS = {
    'add_translation': {
        'lang': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'objects': {
            'type': 'dict',
            'required': True,
            'empty': False
        },
        'force': {
            'type': 'boolean',
            'required': False,
            'empty': True
        }
    },
    'update_translation': {
        'id': {
            'type': 'objectid',
            'required': True,
            'minlength': 12,
            'coerce': ObjectId
        },
        'lang': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'object_key': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'object_data': {
            'type': 'dict',
            'required': False,
            'empty': True
        }
    },
    'get_translation': {
        'id': {
            'type': 'objectid',
            'required': True,
            'minlength': 12,
            'coerce': ObjectId
        }
    },
    'filter_translations': {
        'language': {
            'type': 'string',
            'required': False
        },
        'object_key': {
            'type': 'string',
            'required': False
        },
        'status': {
            'type': 'integer',
            'required': False,
            'empty': True,
            'coerce': int
        }
    },
    'create_language': {
        'alias': {
            'type':   'string',
            'required': True,
            'empty': False
        },
        'label': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'parent': {
            'type': 'objectid',
            'required': False,
            'minlength': 12,
            'coerce': ObjectId
        }
    },
    'update_language': {
        'id': {
            'type': 'objectid',
            'required': True,
            'minlength': 12,
            'coerce': ObjectId
        },
        'alias': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'label': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'parent': {
            'type': 'objectid',
            'required': False,
            'minlength': 12,
            'coerce': ObjectId
        }
    },
    'get_language': {
        'id': {
            'type': 'objectid',
            'required': True,
            'minlength': 12,
            'coerce': ObjectId
        }
    }
}
