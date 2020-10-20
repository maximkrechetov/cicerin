"""Health routes"""

from flask import Blueprint

bp = Blueprint('health', __name__)


@bp.route('/health', methods=('GET',))
def health():
    """
    Health check
    :return: 'OK'
    """
    return 'OK'
