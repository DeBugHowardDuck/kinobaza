from app.extensions.extensions import db

favorites = db.Table(
        "favorites",
        db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
        db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"))
    )