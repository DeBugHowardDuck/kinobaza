from flask import Flask
from flask import jsonify
from marshmallow import ValidationError
from app.models.user import User
from app.extensions.extensions import db, api, ma
from app.views.movies import movie_ns
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.user import user_ns
from app.views.auth import auth_ns
from app.views.auth_info import profile_ns
from app.views.favorites import favorites_ns
from app.utils.logger import setup_logger
from app.utils.error_handlers import register_error_handlers


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kinobaza.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    api.init_app(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns, path="/users")
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(profile_ns, path="/profile")
    api.add_namespace(favorites_ns, path="/favorites")

    ma.init_app(app)
    register_error_handlers(app)
    setup_logger()

    with app.app_context():
        db.create_all()

    from app.models import genre, director, movie

    return app