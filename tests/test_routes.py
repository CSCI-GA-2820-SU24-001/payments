"""
TestYourResourceModel API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from uuid import UUID
from wsgi import app
from service.common import status
from service.common.datetime_utils import datetime_from_str, datetime_to_str
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
    def test_create_promotion(self):
        """Test creating a Promotion"""
        promotion = PromotionFactory()
        print(promotion.serialize())
        response = self.client.post(
            "/promotions", json=promotion.serialize(), content_type="application/json"
        )
        print(response.get_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_promotion = response.get_json()
        self.assertEqual(new_promotion["promotion_name"], promotion.promotion_name)
        self.assertEqual(new_promotion["promotion_scope"], promotion.promotion_scope.name)
        self.assertEqual(new_promotion["promotion_type"], promotion.promotion_type.name)
        self.assertEqual(new_promotion["promotion_value"], promotion.promotion_value)

    def test_create_promotion_missing_data(self):
        """Test creating a Promotion with missing data"""
        response = self.client.post(
            "/promotions", json={}, content_type="application/json"
        )
        print(response.get_data())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_invalid_content_type(self):
        """Test creating a Promotion with an invalid content type"""
        promotion = PromotionFactory()
        response = self.client.post(
            "/promotions", json=promotion.serialize(), content_type="text/plain"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_invalid_data(self):
        """Test creating a Promotion for data validation error"""
        promotion = PromotionFactory()
        new_promotion = promotion.serialize()
        new_promotion['modified_when'] = 'testInvalid'
        response = self.client.post(
            "/promotions", json=new_promotion, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_unexpected_error(self):
        """Test creating a Promotion for an unexpected error"""
        promotion = PromotionFactory()

        # Create mock function to raise connection error on any create
        def mock_create_with_exception():
            raise ConnectionError("Simulated connection error")

        # Store the original create method
        original_create = Promotion.create

        try:
            # Mock the create method to raise an exception
            Promotion.create = mock_create_with_exception

            response = self.client.post(
                "/promotions", json=promotion.serialize(), content_type="application/json"
            )

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Restore the original method
            Promotion.create = original_create

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_with_valid_promotion(self):
        """It should update the model with a valid promotion when a valid object is supplied and return the updated json"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()

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
        db.session.expire_all()
        updated_promotion = Promotion.find(existing_promotion.promotion_id)
        assert updated_promotion.promotion_name == "New Promotion Name"
        assert updated_promotion.start_date == datetime_from_str(
            new_promotion_data["start_date"]
        )
        assert updated_promotion.promotion_scope == PromotionScope.ENTIRE_STORE
        response_json = resp.get_json()
        self.assertEqual(response_json["promotion_id"], updated_promotion.promotion_id)
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

    def test_update_with_invalid_content_type(self):
        """It should return a 415 Invalid content type response"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()

        resp = self.client.put(
            f"/promotions/{existing_promotion.promotion_id}",
            data="12345",
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_update_with_invalid_promotion_id(self):
        """It should not update any model and return a 404 not found when an invalid_promotion_id is supplied"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()

        new_promotion_data = {
            "promotion_name": "New Promotion Name",
            "start_date": "2025-03-03",
            "promotion_scope": "ENTIRE_STORE",
        }
        resp = self.client.put(f"/promotions/{184182325}", json=new_promotion_data)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        db.session.expire_all()
        updated_promotion = Promotion.find(existing_promotion.promotion_id)
        assert updated_promotion.promotion_name != "New Promotion Name"

    def test_update_with_invalid_data(self):
        """It should not update model and return a 400 not found when invalid data is supplied"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()

        new_promotion_data = {
            "promotion_name": "Newest Promotion Name",
            "start_date": "2023/04/21",
            "promotion_scope": "ENTIRE_STORE",
        }
        resp = self.client.put(
            f"/promotions/{existing_promotion.promotion_id}",
            json=new_promotion_data,
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        db.session.expire_all()
        updated_promotion = Promotion.find(existing_promotion.promotion_id)
        self.assertNotEqual(
            updated_promotion.promotion_name, new_promotion_data["promotion_name"]
        )

    def test_update_with_unknown_exception(self):
        """It should not update model and return a 500 when an unknown error occurs"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()

        new_promotion_data = {
            "promotion_name": "Newest Promotion Name",
            "start_date": "2023-04-21",
            "promotion_scope": "ENTIRE_STORE",
        }
        original_update = existing_promotion.update
        try:
            # Create mock function to raise connection error on any update
            def mock_update_with_exception():
                raise ConnectionError

            existing_promotion.update = mock_update_with_exception
            resp = self.client.put(
                f"/promotions/{existing_promotion.promotion_id}",
                json=new_promotion_data,
            )
            self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            db.session.expire_all()
            saved_promotion = Promotion.find(existing_promotion.promotion_id)
            self.assertNotEqual(
                saved_promotion.promotion_name, new_promotion_data["promotion_name"]
            )
        finally:
            existing_promotion.update = original_update

    def test_get_promotion(self):
        """It should Get a single Promotion"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()
        response = self.client.get(
            f"/promotions/{existing_promotion.promotion_id}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["promotion_name"], existing_promotion.promotion_name)
        self.assertEqual(
            data["promotion_description"], existing_promotion.promotion_description
        )
        self.assertEqual(data["promotion_type"], existing_promotion.promotion_type.name)
        self.assertEqual(
            data["promotion_scope"], existing_promotion.promotion_scope.name
        )
        self.assertEqual(
            data["start_date"], datetime_to_str(existing_promotion.start_date)
        )
        self.assertEqual(data["end_date"], datetime_to_str(existing_promotion.end_date))
        self.assertEqual(data["promotion_value"], existing_promotion.promotion_value)
        self.assertEqual(data["promotion_code"], existing_promotion.promotion_code)
        self.assertEqual(UUID(data["created_by"]), existing_promotion.created_by)
        self.assertEqual(UUID(data["modified_by"]), existing_promotion.modified_by)
        self.assertEqual(
            data["created_when"], datetime_to_str(existing_promotion.created_when)
        )
        self.assertEqual(data["modified_when"], existing_promotion.modified_when)

    def test_get_promotion_not_found(self):
        """It should not Get a Promotion thats not found"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()
        response = self.client.get(
            "/promotions/1234567",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_valid_promotion(self):
        """It should delete the model with a valid promotion when a valid object is supplied"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()

        resp = self.client.delete(f"/promotions/{existing_promotion.promotion_id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        db.session.expire_all()
        self.assertIsNone(Promotion.find(existing_promotion.promotion_id))

    def test_delete_with_invalid_promotion_id(self):
        """It should not delete any model and return a 404 not found when an invalid_promotion_id is supplied"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()

        resp = self.client.delete(f"/promotions/{184182325}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        db.session.expire_all()

    def test_delete_with_unknown_exception(self):
        """It should not delete model and return a 400 not found when invalid data is supplied"""
        existing_promotion = PromotionFactory()
        existing_promotion.create()

        original_delete = existing_promotion.delete
        try:
            # Create mock function to raise connection error on any delete
            def mock_delete_with_exception():
                raise ConnectionError

            existing_promotion.delete = mock_delete_with_exception
            resp = self.client.delete(f"/promotions/{existing_promotion.promotion_id}")
            self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            db.session.expire_all()
            saved_promotion = Promotion.find(existing_promotion.promotion_id)
            self.assertIsNotNone(saved_promotion)
        finally:
            existing_promotion.delete = original_delete

    def test_list_all_promotions(self):
        """It should return all promotions in the database"""
        promotion_1 = PromotionFactory()
        promotion_2 = PromotionFactory()
        promotion_1.create()
        promotion_2.create()
        response = self.client.get("/promotions")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    def test_list_all_promotions_with_wrong_method(self):
        """It should return all promotions in the database"""
        promotion_1 = PromotionFactory()
        promotion_2 = PromotionFactory()
        promotion_1.create()
        promotion_2.create()
        response = self.client.put("/promotions")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_all_promotions_with_validation_error(self):
        """It should return a 500 Internal Server Error"""
        promotion_1 = PromotionFactory()
        promotion_2 = PromotionFactory()
        promotion_1.create()
        promotion_2.create()

        original_all = Promotion.all
        try:

            def mock_all():
                raise ConnectionError

            Promotion.all = mock_all
            response = self.client.get("/promotions")
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            Promotion.all = original_all
