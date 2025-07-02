from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
api = Api()
ma = Marshmallow()