""" Application module """

from flask import Flask
from ciceron.models import connect_db
from .router import init_routes

app = Flask(__name__)

connect_db()
init_routes(app)
