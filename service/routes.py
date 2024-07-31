######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Promotion Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Pets from the inventory of pets in the PetShop
"""

from flask import request, abort, jsonify, url_for
from flask import current_app as app  # Import Flask application
from service.models import Promotion
from service.common import status  # HTTP Status Codes

######################################################################
# GET HEALTH CHECK
######################################################################


@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


@app.route("/promotions", methods=["POST"])
def create_promotion():
    """
    Creates a new Promotion
    This endpoint will create a Promotion based on the data in the body that is posted
    """
    app.logger.info("Request to create a Promotion")
    data = request.get_json()
    promotion = Promotion()
    promotion.deserialize(data)
    promotion.create()
    message = promotion.serialize()
    location_url = url_for("read", promotion_id=promotion.promotion_id, _external=True)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


@app.route("/promotions/<int:promotion_id>", methods=["PUT"])
def update(promotion_id):
    """Updates a Promotion with promotion_id with the fields included in the body of the request"""
    app.logger.info(f"Got request to update Promotion with id: {promotion_id}")
    promotion = Promotion.find(promotion_id)
    if not promotion:

        abort_with_error(
            status.HTTP_404_NOT_FOUND, f"Promotion with id: {promotion_id} not found"
        )
    request_json = request.get_json()
    promotion = promotion.deserialize(request_json)
    promotion.update()
    return jsonify(promotion.serialize())


@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def read(promotion_id):
    """
    Read details of specific promotion id
    """
    app.logger.info(
        "Request to Retrieve a promotion with promotion id [%s]", promotion_id
    )
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )
    app.logger.info("Returning promotion: %s", promotion.promotion_name)
    return jsonify(promotion.serialize()), status.HTTP_200_OK


@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete(promotion_id):
    """Deletes a Promotion with promotion_id with the fields included in the body of the request"""
    app.logger.info(f"Got request to delete Promotion with id: {promotion_id}")

    promotion = Promotion.find(promotion_id)
    if promotion:
        promotion.delete()

    app.logger.info(f"Promotion with id {promotion_id} delete complete.")
    return jsonify({}), status.HTTP_204_NO_CONTENT


@app.route("/promotions", methods=["GET"])
def read_all():
    """
    Read details of all promotions matching search criteria
    """
    app.logger.info("Request to Retrieve all promotions with filters: {filters}")
    filters = request.args.to_dict(flat=True)
    to_list_query("promotion_scope", filters)
    to_list_query("promotion_type", filters)
    datetime = filters.get("datetime")
    promotion_scopes = filters.get("promotion_scope")
    promotion_types = filters.get("promotion_types")
    print(datetime, promotion_scopes, promotion_types)

    promotions = Promotion.find_with_filters(filters).all()
    return (
        jsonify([promotion.serialize() for promotion in promotions]),
        status.HTTP_200_OK,
    )


@app.route("/promotions/activate/<int:promotion_id>", methods=["PUT"])
def activate(promotion_id):
    """Activates a Promotion with promotion_id"""
    app.logger.info(f"Got request to activate Promotion with id: {promotion_id}")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort_with_error(
            status.HTTP_404_NOT_FOUND, f"Promotion with id: {promotion_id} not found"
        )
    promotion.active = True
    promotion.update()
    return jsonify(promotion.serialize())


@app.route("/promotions/deactivate/<int:promotion_id>", methods=["PUT"])
def deactivate(promotion_id):
    """Deactivates a Promotion with promotion_id"""
    app.logger.info(f"Got request to deactivate Promotion with id: {promotion_id}")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort_with_error(
            status.HTTP_404_NOT_FOUND, f"Promotion with id: {promotion_id} not found"
        )
    promotion.active = False
    promotion.update()
    app.logger.info(f"Promotion with id {promotion_id} deactivate complete.")
    return jsonify(promotion.serialize())


######################################################################
#  U T I L  F U N C T I O N S
######################################################################


def abort_with_error(error_code, error_msg):
    """Aborts a request with a specific error code and message

    Args:
        error_code (int): error code number
        error_msg (str): description of the error
    """
    app.logger.error(error_msg)
    abort(error_code, error_msg)


def to_list_query(key, data):
    """Converts a value in a dictionary to a list from a comma-separated string if it exists

    Args:
        key (str): the key to be converted
        data (dict): the dict to convert it in
    """
    if key in data:
        data[key] = str.split(data[key], ",")
