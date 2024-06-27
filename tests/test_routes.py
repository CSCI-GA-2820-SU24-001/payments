"""
TestYourResourceModel API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.common.datetime_utils import datetime_from_str
from service.models import db, Promotion, PromotionScope
from tests.factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_with_valid_promotion(self):
        """It should update the model with a valid promotion when a valid object is supplied and return the updated json"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()
        original_find = Promotion.find
        try:
            # Stub class method for find
            def mock_find(id):
                return (
                    existing_promotion
                    if id == existing_promotion.promotion_id
                    else None
                )

            Promotion.find = mock_find
            # End of stub
            new_promotion_data = {
                "promotion_name": "New Promotion Name",
                "start_date": "2025-03-03",
                "promotion_scope": "ENTIRE_STORE",
            }
            resp = self.client.put(
                f"/promotions/{existing_promotion.promotion_id}",
                json=new_promotion_data,
            )
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            assert existing_promotion.promotion_name == "New Promotion Name"
            assert existing_promotion.start_date == datetime_from_str(
                new_promotion_data["start_date"]
            )
            assert existing_promotion.promotion_scope == PromotionScope.ENTIRE_STORE
            response_json = resp.get_json()
            self.assertEqual(
                response_json["promotion_id"], existing_promotion.promotion_id
            )
            self.assertEqual(
                response_json["promotion_name"], new_promotion_data["promotion_name"]
            )
            self.assertEqual(
                response_json["promotion_value"], existing_promotion.promotion_value
            )
            self.assertEqual(
                datetime_from_str(response_json["start_date"]),
                datetime_from_str(new_promotion_data["start_date"]),
            )
            self.assertEqual(
                response_json["promotion_scope"], new_promotion_data["promotion_scope"]
            )

        finally:
            Promotion.find = original_find

    def test_update_with_invalid_promotion_id(self):
        """It should not update model and return a 404 not found when an invalid_promotion_id is supplied"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()
        original_find = Promotion.find
        try:
            # Stub class method for find
            def mock_find(id):
                return (
                    existing_promotion
                    if id == existing_promotion.promotion_id
                    else None
                )

            Promotion.find = mock_find
            # End of stub
            new_promotion_data = {
                "promotion_name": "New Promotion Name",
                "start_date": "2025-03-03",
                "promotion_scope": "ENTIRE_STORE",
            }
            resp = self.client.put(
                f"/promotions/{18418231125}", json=new_promotion_data
            )
            self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
            assert existing_promotion.promotion_name != "New Promotion Name"

        finally:
            Promotion.find = original_find

    def test_update_with_invalid_data(self):
        """It should not update model and return a 400 not found when invalid data is supplied"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()
        print(existing_promotion.promotion_id)
        original_find = Promotion.find
        try:
            # Stub class method for find
            def mock_find(id):
                print(f"Looking for id {id}")
                return (
                    existing_promotion
                    if id == existing_promotion.promotion_id
                    else None
                )

            Promotion.find = mock_find
            # End of stub
            new_promotion_data = {
                "promotion_name": "New Promotion Name",
                "start_date": "2023/04/21",
                "promotion_scope": "ENTIRE_STORE",
            }
            resp = self.client.put(
                f"/promotions/{existing_promotion.promotion_id}",
                json=new_promotion_data,
            )
            self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        finally:
            Promotion.find = original_find
