""" Routes loader module """

import pkgutil
from importlib import import_module
from os.path import join, dirname
from flask import Blueprint


def init_routes(app):
    """
    Initialization of Flask routes
    :param app: Flask App
    :return:
    """
    rel = join(dirname(__file__), 'routes')

    for (_, name, _) in pkgutil.iter_modules([rel]):
        imported = import_module('ciceron.http.routes.' + name)

        if hasattr(imported, 'bp') and isinstance(imported.bp, Blueprint):
            app.register_blueprint(imported.bp)
