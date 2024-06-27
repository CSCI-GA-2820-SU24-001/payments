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
from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  YourResourceModel   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotions(TestCase):
    """Test Cases for YourResourceModel Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
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

    # Todo: Add your test cases here...

    def test_serialize_promotion(self):
        """ It should deserialize a Promotion into a dict"""
        test_promotion = PromotionFactory()
        serialized = test_promotion.serialize()
        assert serialized["promotion_id"] == test_promotion.promotion_id
        assert serialized["promotion_name"] == test_promotion.promotion_name
        assert serialized["promotion_type"] == test_promotion.promotion_type
        assert serialized["promotion_scope"] == test_promotion.promotion_scope
        assert serialized["start_date"] == test_promotion.start_date
        assert serialized["end_date"] == test_promotion.end_date
        assert serialized["promotion_value"] == test_promotion.promotion_value
        assert serialized["promotion_code"] == test_promotion.promotion_code
        assert serialized["created_by"] == test_promotion.created_by
        assert serialized["modified_by"] == test_promotion.modified_by
        assert serialized["created_when"] == test_promotion.created_when
        assert serialized["modified_when"] == test_promotion.modified_when

    def test_serialized_promotion_with_missing_fields(self):
        """ It should deserialize a Promotion into a dict with some fields as None"""
        test_promotion = PromotionFactory()
        test_promotion.promotion_name = None
        test_promotion.modified_when = None
        serialized = test_promotion.serialize()
        assert serialized["promotion_id"] == test_promotion.promotion_id
        assert serialized["promotion_type"] == test_promotion.promotion_type
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
        promotion.deserialize(promotion_json)
        assert promotion.promotion_id == 123
        assert promotion.promotion_name == "abcPromotion"
        assert promotion.promotion_description == "abcPromotionDescription"
        assert promotion.promotion_type == PromotionType.PERCENTAGE
        assert promotion.promotion_scope == PromotionScope.PRODUCT_ID
        assert promotion.start_date == datetime(2021, 1, 1, 0, 0)
        assert promotion.end_date == datetime(2021, 12, 31, 0, 0)
        assert promotion.promotion_value == 10.0
        assert promotion.promotion_code == "abcPromotionCode"
        assert promotion.created_by == default_uuid
        assert promotion.modified_by == default_uuid
        assert promotion.created_when == datetime(2021, 1, 1, 0, 0)
        assert promotion.modified_when == datetime(2021, 1, 1, 0, 0)

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

    def test_create_promotion(self):
        """It should create a Promotion"""
        test_promotion = PromotionFactory()

        test_promotion.create()
        assert test_promotion.promotion_name == "some_promotion"
        assert test_promotion.created_by == test_promotion.created_by
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
