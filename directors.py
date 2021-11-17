"""
This is the directors module and supports all the REST actions for the
directors data
"""

from flask import make_response, abort
from config import db
from models import Director, DirectorSchema, Movie


def read_all():
    """
    This function responds to a request for /api/directors
    with the complete lists of directors
    :return:        json string of list of directors
    """
    directors = Director.query.order_by(Director.id).all()

    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(directors)
    return data


def read_one(id):
    """
    This function responds to a request for /api/directors/{id}
    with one matching person from people
    :param id:          Id of director to find
    :return:            director matching id
    """
    director = (
        Director.query.filter(Director.id == id)
        .outerjoin(Movie)
        .one_or_none()
    )

    if director is not None:

        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return data

    else:
        abort(404, f"Director not found for Id: {id}")


def create(director):
    """
    This function creates a new director in the directors structure
    based on the passed in director data
    :param director:    director to create in directors structure
    :return:            201 on success, 406 on director exists
    """
    
    name = director.get("name")
    gender = director.get("gender")
    uid = director.get("uid")
    department = director.get("department")

    existing_director = (
        Director.query.filter(Director.name == name)
        .filter(Director.gender == gender)
        .filter(Director.uid == uid)
        .filter(Director.department == department)
        .one_or_none()
    )

    if existing_director is None:

        schema = DirectorSchema()
        new_director = schema.load(director, session=db.session)

        db.session.add(new_director)
        db.session.commit()

        data = schema.dump(new_director)

        return data, 201

    else:
        abort(409, f"Director {name} exists already")


def update(id, director):
    """
    This function updates an existing director in the directors structure
    :param id:          Id of the director to update in the directors structure
    :param director:    director to update
    :return:            updated director structure
    """
    update_director = Director.query.filter(
        Director.id == id
    ).one_or_none()

    if update_director is not None:

        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        update.id = update_director.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_director)

        return data, 200

    else:
        abort(404, f"Director not found for Id: {id}")


def delete(id):
    """
    This function deletes a director from the directors structure
    :param id:          Id of the director to delete
    :return:            200 on successful delete, 404 if not found
    """
    director = Director.query.filter(Director.id == id).one_or_none()

    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {id} deleted", 200)

    else:
        abort(404, f"Director not found for Id: {id}")


def read_by_nameprefix(nameprefix):
    """
    This function responds to a request for /api/directors/nameprefix/{nameprefix}
    with the complete lists of directors who have the desired name prefix
    :param nameprefix:          Name prefix of the director to get
    :return:                    json string of list of directors with desired name prefix
    """
    directors = Director.query.filter(Director.name.like(f'{nameprefix}%')).all()

    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(directors)
    return data


def read_by_gender(gender):
    """
    This function responds to a request for /api/directors/gender/{gender}
    with the complete lists of directors with specific gender
    :param gender:          Gender of the director to get
    :return:                json string of list of directors with specific gender
    """
    directors = Director.query.filter(Director.gender == gender).all()

    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(directors)
    return data


def delete_by_name(name):
    """
    This function deletes a director from the directors structure based on name
    :param name:        Name of the director to delete
    :return:            200 on successful delete, 404 if not found
    """
    director = Director.query.filter(Director.name == name).one_or_none()

    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {name} deleted", 200)

    else:
        abort(404, f"Director not found for name: {name}")