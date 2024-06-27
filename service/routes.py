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
Pet Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Pets from the inventory of pets in the PetShop
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Promotion, DataValidationError
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


@app.route("/promotions/>int:promotion_id", methods=["PUT"])
def update(promotion_id):
    """Updates a Promotion with promotion_id with the fields included in the body of the request"""
    app.logger.info(f"Got request to update Promotion with id: {promotion_id}")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort_with_error(status.HTTP_404_NOT_FOUND,
                         f"Promotion with id: {promotion_id} not found")
    try:
        request_json = request.get_json()
        promotion = promotion.deserialize(request_json)
        promotion.update()
    except DataValidationError as error:
        abort_with_error(status.HTTP_400_BAD_REQUEST, f"Bad Request: {error}")
    except Exception as error:  # pylint: disable=broad-except
        abort_with_error(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred : {error}")

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
