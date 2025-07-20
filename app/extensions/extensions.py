from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
api = Api(
    title="КиноБаза API",
    version="1.0",
    description="Документация к API КиноБазы",
    doc="/",
    doc_expansion="none",
    hide_models=True
)
ma = Marshmallow()