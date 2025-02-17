#!/usr/bin/python3

"""
this view handles default responses from the API

Authors: Bradley Dillion Gilden & Kevin KevCare Mokobane
Date: 29-10-2023
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Returns a JSON of an obj count of all tables in the database/file storage
    """
    return jsonify({
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    })
