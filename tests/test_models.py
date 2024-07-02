"""
Test cases for Pet Model
"""

import os
import logging
import uuid
from datetime import datetime
from unittest import TestCase
from wsgi import app
from service.models import Promotion, DataValidationError, PromotionScope, PromotionType, db
from service.common.datetime_utils import datetime_to_str
from .factories import PromotionFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Promotions   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods,duplicate-code
class Promotions(TestCase):
    """Test Cases for Promotion Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_serialize_promotion(self):
        """ It should deserialize a Promotion into a dict"""
        test_promotion = PromotionFactory()
        serialized = test_promotion.serialize()
        assert serialized["promotion_id"] == test_promotion.promotion_id
        assert serialized["promotion_name"] == test_promotion.promotion_name
        assert serialized["promotion_type"] == test_promotion.promotion_type.name
        assert serialized["promotion_scope"] == test_promotion.promotion_scope.name
        assert serialized["start_date"] == datetime_to_str(test_promotion.start_date)
        assert serialized["end_date"] == datetime_to_str(test_promotion.end_date)
        assert serialized["promotion_value"] == test_promotion.promotion_value
        assert serialized["promotion_code"] == test_promotion.promotion_code
        assert serialized["created_by"] == test_promotion.created_by
        assert serialized["modified_by"] == test_promotion.modified_by
        assert serialized["created_when"] == datetime_to_str(test_promotion.created_when)
        assert serialized["modified_when"] is None

    def test_serialize_promotion_2(self):
        """It should deserialize a Promotion into a dict"""
        test_promotion = PromotionFactory()
        serialized = test_promotion.serialize()
        assert serialized["promotion_id"] == test_promotion.promotion_id
        assert serialized["promotion_name"] == test_promotion.promotion_name
        assert serialized["promotion_type"] == test_promotion.promotion_type.name
        assert serialized["promotion_scope"] == test_promotion.promotion_scope.name
        assert serialized["start_date"] == datetime_to_str(test_promotion.start_date)
        assert serialized["end_date"] == datetime_to_str(test_promotion.end_date)
        assert serialized["promotion_value"] == test_promotion.promotion_value
        assert serialized["promotion_code"] == test_promotion.promotion_code
        assert serialized["created_by"] == test_promotion.created_by
        assert serialized["modified_by"] == test_promotion.modified_by
        assert serialized["created_when"] == datetime_to_str(
            test_promotion.created_when
        )
        assert serialized["modified_when"] is None

    def test_serialized_promotion_with_missing_fields(self):
        """ It should deserialize a Promotion into a dict with some fields as None"""
        test_promotion = PromotionFactory()
        test_promotion.promotion_name = None
        test_promotion.modified_when = None
        serialized = test_promotion.serialize()
        assert serialized["promotion_id"] == test_promotion.promotion_id
        assert serialized["promotion_type"] == test_promotion.promotion_type.name
        assert serialized["promotion_name"] is None
        assert serialized["modified_when"] is None

    def test_deserialize_promotion(self):
        """It should deserialize a promotion json into a valid Promotion"""
        default_uuid = uuid.uuid4()
        promotion_json = {
            "promotion_id": 123,
            "promotion_name": "abcPromotion",
            "promotion_description": "abcPromotionDescription",
            "promotion_type": "PERCENTAGE",
            "promotion_scope": "PRODUCT_ID",
            "start_date": "2021-01-01",
            "end_date": "2021-12-31",
            "promotion_value": 10.0,
            "promotion_code": "abcPromotionCode",
            "created_by": default_uuid,
            "modified_by": default_uuid,
            "created_when": "2021-01-01",
            "modified_when": "2021-01-01",
        }
        promotion = Promotion()
        result = promotion.deserialize(promotion_json)
        assert result.promotion_id == 123
        assert result.promotion_name == "abcPromotion"
        assert result.promotion_description == "abcPromotionDescription"
        assert result.promotion_type == PromotionType.PERCENTAGE
        assert result.promotion_scope == PromotionScope.PRODUCT_ID
        assert result.start_date == datetime(2021, 1, 1, 0, 0)
        assert result.end_date == datetime(2021, 12, 31, 0, 0)
        assert result.promotion_value == 10.0
        assert result.promotion_code == "abcPromotionCode"
        assert result.created_by == default_uuid
        assert result.modified_by == default_uuid
        assert result.created_when == datetime(2021, 1, 1, 0, 0)
        assert result.modified_when == datetime(2021, 1, 1, 0, 0)

    def test_deserialize_invalid_promotion(self):
        """ It should throw an exception for any invalid formats """
        invalid_json_type = {
            "promotion_id": 123,
            "promotion_name": "abcPromotion",
            "promotion_description": "abcPromotionDescription",
            "promotion_type": "InvalidFormat",
        }
        invalid_json_scope = {
            "promotion_id": 123,
            "promotion_name": "abcPromotion",
            "promotion_description": "abcPromotionDescription",
            "promotion_scope": "SOME UNKNOWN",
        }
        invalid_json_date = {
            "promotion_id": 123,
            "promotion_name": "abcPromotion",
            "promotion_description": "abcPromotionDescription",
            "promotion_scope": "SOME UNKNOWN",
            "start_date": "abc123"
        }
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, invalid_json_type)
        self.assertRaises(DataValidationError, promotion.deserialize, invalid_json_scope)
        self.assertRaises(DataValidationError, promotion.deserialize, invalid_json_date)
        assert promotion.promotion_name is None
        assert promotion.promotion_description is None
        assert promotion.promotion_scope is None
        assert promotion.start_date is None

    def test_deserialize_with_errors(self):
        """It should raise a DataValidationError"""
        promotion_json = {
            "promotion_id": 123,
            "promotion_name": "abcPromotion"
        }
        promotion = Promotion()
        original_deserialize_with_default = promotion.deserialize_with_default
        try:
            # Type Error
            def type_error_deserialize(key, data, default, deserializer=None):
                raise TypeError("Some bad type")
            promotion.deserialize_with_default = type_error_deserialize
            self.assertRaises(DataValidationError, promotion.deserialize, promotion_json)

            # Attribute Error
            def attribute_error_deserialize(key, data, default, deserializer=None):
                raise AttributeError("Some bad attribute")
            promotion.deserialize_with_default = attribute_error_deserialize
            self.assertRaises(
                DataValidationError, promotion.deserialize, promotion_json
            )

        finally:
            promotion.deserialize_with_default = original_deserialize_with_default

    def test_create_promotion(self):
        """It should create a Promotion"""
        test_promotion = PromotionFactory()

        test_promotion.create()
        assert test_promotion.promotion_name == "some_promotion"
        assert test_promotion.created_by == test_promotion.created_by
        # Refresh session to get object from DB. Committed objects should remain.
        db.session.expire_all()
        found = Promotion.all()
        self.assertEqual(len(found), 1)
        data = Promotion.find(test_promotion.promotion_id)
        self.assertEqual(data.promotion_name, test_promotion.promotion_name)
        self.assertEqual(data.start_date, datetime(2025, 1, 1, 0, 0))

    def test_create_invalid_promotion(self):
        """It should throw a DataValidationError"""
        test_promotion = PromotionFactory()
        test_promotion.start_date = "abcadw"
        self.assertRaises(DataValidationError, test_promotion.create)

    def test_update_promotion(self):
        """It should update an existing promotion"""
        test_promotion = PromotionFactory()
        test_promotion.create()
        test_promotion.promotion_name = "Updated Name"
        test_promotion.update()

        db.session.expire_all()
        updated_promotion = Promotion.find(test_promotion.promotion_id)
        assert updated_promotion.promotion_name == "Updated Name"

    def test_update_invalid_promotion(self):
        """ It should not update promotion and raise DataValidationError"""
        test_promotion = PromotionFactory()
        test_promotion.create()
        test_promotion.start_date = "InvalidDateFormat"
        test_promotion.promotion_name = "Updated Name"
        self.assertRaises(DataValidationError, test_promotion.update)

        db.session.expire_all()
        updated_promotion = Promotion.find(test_promotion.promotion_id)
        self.assertNotEqual(updated_promotion.promotion_name, "Updated Name")

    def test_delete_promotion(self):
        """It should delete an existing promotion"""
        test_promotion = PromotionFactory()
        test_promotion.create()
        test_promotion.delete()
        db.session.expire_all()
        deleted_promotion = Promotion.find(test_promotion.promotion_id)
        self.assertIsNone(deleted_promotion)

    def test_delete_invalid_promotion(self):
        """It should throw a DataValidationError"""
        test_promotion = PromotionFactory()
        test_promotion.start_date = "RandomStartDate"
        self.assertRaises(DataValidationError, test_promotion.delete)
        deleted_promotion = Promotion.find(test_promotion.promotion_id)
        self.assertIsNone(deleted_promotion)
