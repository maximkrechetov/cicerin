"""Docs routes"""

from os.path import join, dirname, abspath
from flask import Blueprint, jsonify, send_file

import yaml

__DOCS_ROOT = abspath(join(dirname(__file__), '../../../docs/swagger'))
bp = Blueprint('docs', __name__, url_prefix='/docs')


@bp.route('/', methods=['GET'])
def get_doc_ui():
    """
    Returns API Documentation page
    :return:
    """
    return send_file(join(__DOCS_ROOT, 'ui.html'))


@bp.route('/api.json', methods=['GET'])
def get_api_json():
    """
    Returns API documentation in JSON
    :return:
    """
    with open(join(__DOCS_ROOT, 'api.yaml'), 'r') as file:
        api = yaml.load(file)

    return jsonify(api)
