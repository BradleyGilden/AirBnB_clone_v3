#!/usr/bin/python3

"""
a view for City objects that handles all default RESTFul API actions

Author: Bradley Dillion Gilden
Date: 27-10-2023
"""


from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, make_response, request


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def cities_per_state(state_id):
    """retrieves of a list of all city objects for a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """retrieves a specific city obj"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_city(city_id):
    """deletes specific city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """adds new city object to filestorage/database"""
    json_body = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if json_body.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    city = City(**json_body)
    city.state_id = state.id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """updates city object on filestorage/database"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in json_body.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
