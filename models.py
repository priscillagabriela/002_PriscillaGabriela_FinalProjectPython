from datetime import datetime
from config import db, ma
from marshmallow import fields

class Director(db.Model):
    __tablename__ = 'directors'
    name = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.String(50))

    movies = db.relationship(
        'Movie',
        backref='director',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Movie.id)'
    )

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(1500))
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.String(10))
    revenue = db.Column(db.Integer)
    title = db.Column(db.String(1500))
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.String(2000))
    tagline = db.Column(db.String(1500))
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

class DirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Director
        sqla_session = db.session
        load_instance = True

    movies = fields.Nested('DirectorMovieSchema', default=[], many=True)

class DirectorMovieSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int()
    release_date = fields.Str()
    revenue = fields.Int()
    title = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    overview = fields.Str()
    tagline = fields.Str()
    uid = fields.Int()
    director_id = fields.Int()


class MovieSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movie
        sqla_session = db.session
        load_instance = True

    director = fields.Nested("MovieDirectorSchema", default=None)


class MovieDirectorSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    name = fields.Str()
    id = fields.Int()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()