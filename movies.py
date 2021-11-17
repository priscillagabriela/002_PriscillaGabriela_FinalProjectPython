"""
This is the movies module and supports all the REST actions for the
movies
"""

from flask import make_response, abort
from config import db
from models import Director, Movie, MovieSchema


def read_all():
    """
    This function responds to a request for /api/movies
    with the complete list of movies, sorted by id
    :return:                json list of all movies for all directors
    """
    movies = Movie.query.order_by(db.desc(Movie.id)).all()

    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data


def read_one(director_id, id):
    """
    This function responds to a request for
    /api/directors/{director_id}/movies/{id}
    with one matching note for the associated person
    :param director_id:         Id of director the movie is related to
    :param id_id:               Id of the movie
    :return:                    json string of movie contents
    """
    movie = (
        Movie.query.join(Director, Director.id == Movie.director_id)
        .filter(Director.id == director_id)
        .filter(Movie.id == id)
        .one_or_none()
    )

    if movie is not None:
        movie_schema = MovieSchema()
        data = movie_schema.dump(movie)
        return data

    else:
        abort(404, f"Movie not found for Id: {id}")


def create(director_id, movie):
    """
    This function creates a new movie related to the passed in director id.
    :param director_id:     Id of the director the movie is related to
    :param note:            The JSON containing the movie data
    :return:                201 on success
    """
    director = Director.query.filter(Director.id == director_id).one_or_none()

    if director is None:
        abort(404, f"Director not found for Id: {director_id}")

    schema = MovieSchema()
    new_movie = schema.load(movie, session=db.session)

    director.movies.append(new_movie)
    db.session.commit()

    data = schema.dump(new_movie)

    return data, 201


def update(director_id, id, movie):
    """
    This function updates an existing movie related to the passed in
    director id.
    :param director_id:         Id of the director the movie is related to
    :param id:                  Id of the movie to update
    :param movie:               The JSON containing the movie data
    :return:                    200 on success
    """
    update_movie = (
        Movie.query.filter(Director.id == director_id)
        .filter(Movie.id == id)
        .one_or_none()
    )

    if update_movie is not None:

        schema = MovieSchema()
        update = schema.load(movie, session=db.session)

        update.id = update_movie.id
        update.director_id = update_movie.director_id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_movie)

        return data, 200

    else:
        abort(404, f"Movie not found for Id: {id}")


def delete(director_id, id):
    """
    This function deletes a movie from the movie structure
    :param director_id:     Id of the director the movie is related to
    :param id:              Id of the movie to delete
    :return:                200 on successful delete, 404 if not found
    """
    movie = (
        Movie.query.filter(Director.id == director_id)
        .filter(Movie.id == id)
        .one_or_none()
    )

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {id} deleted".format(id=id), 200
        )

    else:
        abort(404, f"Movie not found for Id: {id}")

    
def read_most_popular_movie(limit):
    """
    This function responds to a request for /api/movies/popularity/{limit}
    with the list of movies based on highest popularity
    :param limit:           Limit of movie to be displayed based on highest popularity
    :return:                json list of movies based on highest popularity and desired limit
    """
    movies = Movie.query.order_by(Movie.popularity.desc()).limit(limit).all()

    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data


def read_by_release_year(release_year):
    """
    This function responds to a request for /api/movies/releaseyear/{release_year}
    with the list of movies based on particular release year
    :param release_year:    Release year of the movie to get
    :return:                json list movies based on particular release_year
    """
    movies = Movie.query.filter(Movie.release_date.like(f'{release_year}%')).all()

    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data


def delete_by_orititle(original_title):
    """
    This function deletes a movie from the movie structure
    :param original_title:      Original title of the movie to delete
    :return:                    200 on successful delete, 404 if not found
    """
    movie = (
        Movie.query.filter(Movie.original_title == original_title)
        .one_or_none()
    )

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {orititle} deleted".format(orititle=original_title), 200
        )

    else:
        abort(404, f"Movie not found for title: {original_title}")



