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
from flask_restx import Resource, fields, reqparse
from service.models import Promotion, PromotionType, PromotionScope
from service.common import status  # HTTP Status Codes
from . import api

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")

######################################################################
# GET HEALTH CHECK
######################################################################


@api.route("/health")
class HealthResource(Resource):
    def get(self):
        """Let them know our heart is still beating"""
        return jsonify(status=200, message="Healthy")


######################################################################
# M O D E L S
######################################################################

class NullableString(fields.String):
    """ Input class which expects a string or null value """
    __schema_type__ = ["string", "null"]
    __schema_example__ = "nullable string"


class FixedNumber(fields.Fixed):
    def fixed_format(self, value):
        return super().format(value)
    
    def format(self, value):
        return float(self.fixed_format(value))


create_model = api.model(
    "Promotion",
    {
        "promotion_name": fields.String(
            required=True, description="The name of the Promotion"
        ),
        "promotion_description": fields.String(
            required=True, description="The description of the Promotion"
        ),
        "promotion_type": fields.String(
            required=True,
            enum=PromotionType._member_names_,
            description="The type of Promotion (e.g. discount, buy one get one)",
        ),
        "promotion_scope": fields.String(
            required=True,
            enum=PromotionScope._member_names_,
            description="The scope of Promotion (e.g. product_id, entire_store)",
        ),
        "start_date": fields.DateTime(
            required=True, description="The start date of the Promotion"
        ),
        "end_date": fields.DateTime(
            required=True, description="The end date of the Promotion"
        ),
        "promotion_value": FixedNumber(
            decimals=2,
            required=True,
            description="The value of Promotion (Takes different values depending on the type)",
        ),
        "promotion_code": NullableString(
            required=False,
            description="The promotional code used to apply the promotion",
        ),
        "created_by": fields.String(
            required=True, description="The user who created the Promotion"
        ),
        "active": fields.Boolean(
            required=False, description="Is the Promotion activated?", default=False
        ),
    },
)

update_model = api.model(
    "Promotion",
    {
        "promotion_name": fields.String(
            required=False, description="The name of the Promotion"
        ),
        "promotion_description": fields.String(
            required=False, description="The description of the Promotion"
        ),
        "promotion_type": fields.String(
            required=False,
            enum=PromotionType._member_names_,
            description="The type of Promotion (e.g. discount, buy one get one)",
        ),
        "promotion_scope": fields.String(
            required=False,
            enum=PromotionScope._member_names_,
            description="The scope of Promotion (e.g. product_id, entire_store)",
        ),
        "start_date": fields.DateTime(
            required=False, description="The start date of the Promotion"
        ),
        "end_date": fields.DateTime(
            required=False, description="The end date of the Promotion"
        ),
        "promotion_value": FixedNumber(
            decimals=2,
            required=False,
            description="The value of Promotion (Takes different values depending on the type)",
        ),
        "promotion_code": NullableString(
            required=False,
            description="The promotional code used to apply the promotion",
        ),
        "created_by": fields.String(
            required=False, description="The user who created the Promotion"
        ),
        "active": fields.Boolean(
            required=False, description="Is the Promotion activated?", default=False
        ),
    },
)

promotion_model = api.inherit(
    "Promotion",
    create_model,
    {
        "promotion_id": fields.Integer(
            required=True, description="The unique id assigned to the Promotion"
        ),
        "created_by": fields.String(
            required=True, description="The user who created the Promotion"
        ),
        "created_when": fields.DateTime(
            required=False, description="When the Promotion was created"
        ),
        "modified_by": fields.String(
            required=False, description="The most recent user who updated the Promotion"
        ),
        "modified_when": fields.DateTime(
            required=False, description="When the Promotion was last updated"
        ),
    },
)

promotion_args = reqparse.RequestParser()
promotion_args.add_argument("datetime", type=str, required=False, help="The datetime of the promotion in ISO format")
promotion_args.add_argument("promotion_scope", type=str, required=False, help="The scopes of promotions requested")
promotion_args.add_argument("promotion_type", type=str, required=False, help="The types of promotions requested")


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################
@api.route("/promotions/<promotion_id>", strict_slashes=False)
@api.param("promotion_id", "The Promotion identifier")
class PromotionResource(Resource):
    """
    PromotionResource class

    Allows the manipulation of a single Promotion
    GET /promotion/{promotion_id} - Get details of a Promotion with the promotion_id
    PUT /promotion/{promotion_id} - Update a Promotion with the promotion_id
    DELETE /promotion/{promotion_id} - Delete a Promotion with the promotion_id
    """

    @api.doc("update_promotion")
    @api.response(400, "The posted Promotion data was not valid")
    @api.response(404, "Promotion not found")
    @api.marshal_with(promotion_model)
    @api.expect(update_model)
    def put(self, promotion_id):
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
        return promotion.serialize()

    @api.doc("get_promotion")
    @api.response(404, "Promotion not found")
    @api.marshal_with(promotion_model)
    def get(self, promotion_id):
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
        return promotion.serialize(), status.HTTP_200_OK

    @api.doc("delete_promotion")
    @api.response(204, "Promotion deleted")
    @api.response(404, "Promotion not found")
    def delete(self, promotion_id):
        """Deletes a Promotion with promotion_id with the fields included in the body of the request"""
        app.logger.info(f"Got request to delete Promotion with id: {promotion_id}")

        promotion = Promotion.find(promotion_id)
        if promotion:
            promotion.delete()

        app.logger.info(f"Promotion with id {promotion_id} delete complete.")
        return {}, status.HTTP_204_NO_CONTENT


@api.route("/promotions", strict_slashes=False)
class PromotionCollection(Resource):
    """Handles all interactions with collections of Promotions"""

    @api.doc("query_promotions")
    @api.expect(promotion_args, validate=True)
    @api.marshal_list_with(promotion_model)
    def get(self):
        """
        Read details of all promotions matching search criteria
        """
        app.logger.info("Request to Retrieve all promotions with filters: {filters}")
        filters = promotion_args.parse_args()
        to_list_query("promotion_scope", filters)
        to_list_query("promotion_type", filters)
        promotions = Promotion.find_with_filters(filters).all()
        return (
            [promotion.serialize() for promotion in promotions],
            status.HTTP_200_OK,
        )

    @api.doc("create_promotion")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model, validate=True)
    @api.marshal_with(promotion_model, code=201)
    def post(self):
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
        location_url = api.url_for(
            PromotionResource, promotion_id=promotion.promotion_id, _external=True
        )
        return message, status.HTTP_201_CREATED, {"Location": location_url}


@api.route("/promotions/activate/<promotion_id>")
@api.param("promotion_id", "The Promotion identifier")
class ActivateResource(Resource):
    """Activate actions on a promotion
    
    PUT /promotions/activate/{promotion_id} - Activate a Promotion with the promotion_id
    """
    @api.doc("activate_promotion")
    @api.response(404, "Promotion not found")
    @api.response(200, "Promotion Activated")
    @api.marshal_with(promotion_model)
    def put(self, promotion_id):
        """Activates a Promotion with promotion_id"""
        app.logger.info(f"Got request to activate Promotion with id: {promotion_id}")
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort_with_error(
                status.HTTP_404_NOT_FOUND, f"Promotion with id: {promotion_id} not found"
            )
        promotion.active = True
        promotion.update()
        return promotion.serialize()


@api.route("/promotions/deactivate/<promotion_id>")
@api.param("promotion_id", "The Promotion identifier")
class DeactivateResource(Resource):
    """Deactivate actions on a promotion

    PUT /promotions/deactivate/{promotion_id} - Deactivate a Promotion with the promotion_id
    """
    @api.doc("activate_promotion")
    @api.response(404, "Promotion not found")
    @api.response(200, "Promotion Deactivated")
    @api.marshal_with(promotion_model)
    def put(self, promotion_id):
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
        return promotion.serialize()


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
    if key in data and data[key] is not None:
        data[key] = str.split(data[key], ",")
