#!/usr/bin/python3

"""
a view for Place->Amenity relationship that handles all default RESTFul
API actions

Authors: Bradley Dillion Gilden & Kevin KevCare Mokobane
Date: 29-10-2023
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def place_amenity(place_id):
    """retrieves of a list of all place objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([obj.to_dict() for obj in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place_amenity(place_id, amenity_id):
    """retrieves specific place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    for i in range(len(place.amenities)):
        if place.amenities[i] == amenity:
            place.amenities[i].delete()
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """deletes specific place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place.amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
