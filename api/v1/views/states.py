#!/usr/bin/python3

"""
a view for State objects that handles all default RESTFul API actions

Author: Bradley Dillion Gilden
Date: 26-10-2023
"""


from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, make_response, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """retrieves of a list of all state objects"""
    return jsonify([obj.to_dict() for obj in storage.all('State').values()])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """retrieves specific state obj"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_state(state_id):
    """deletes specific state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """adds new state object to filestorage/database"""
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if json_body.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**json_body)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """adds new state object to filestorage/database"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in json_body.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
