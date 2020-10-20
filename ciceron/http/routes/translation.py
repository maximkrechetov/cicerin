"""Translation routes"""


from flask import Blueprint
from flask_restful import Api

from ciceron.http.resources import TranslationResource

bp = Blueprint('translation', __name__)

api_bp = Api(bp)
api_bp.add_resource(TranslationResource, '/translate')
