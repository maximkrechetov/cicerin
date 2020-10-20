"""Admin API routes"""

from flask import Blueprint
from flask_restful import Api

from ciceron.http.resources import LanguageResource, TranslationAdminResource

bp = Blueprint('api', __name__, url_prefix='/api')

api_bp = Api(bp)

api_bp.add_resource(LanguageResource, '/language', '/language/<string:id>')
api_bp.add_resource(TranslationAdminResource, '/translation', '/translation/<string:id>')
