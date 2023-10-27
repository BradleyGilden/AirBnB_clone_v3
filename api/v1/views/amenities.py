#!/usr/bin/python3

"""
a view for Amenity objects that handles all default RESTFul API actions

Author: Bradley Dillion Gilden
Date: 26-10-2023
"""


from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, make_response, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenities():
    """retrieves of a list of all amenity objects"""
    return jsonify([obj.to_dict() for obj in storage.all('Amenity').values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """retrieves specific amenity obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_amenity(amenity_id):
    """deletes specific state object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """adds new state object to filestorage/database"""
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if json_body.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenity = Amenity(**json_body)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def put_amenity(amenity_id):
    """adds new state object to filestorage/database"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in json_body.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
