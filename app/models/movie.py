from app.extensions.extensions import db

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(512))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)

    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"))

    genre = db.relationship("Genre", backref="movies")
    director = db.relationship("Director", backref="movies")


    def __repr__(self):
        return f"<Movie {self.id}: {self.title}>"
