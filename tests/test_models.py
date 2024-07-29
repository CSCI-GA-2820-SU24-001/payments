"""
Test cases for Pet Model
"""

import os
import logging
import uuid
from datetime import datetime
from unittest import TestCase
from wsgi import app
from service.models import (
    Promotion,
    DataValidationError,
    PromotionScope,
    PromotionType,
    db,
)
from service.common.datetime_utils import datetime_to_str
from .factories import PromotionFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@postgres:5432/testdb"
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

        assert serialized["modified_when"] is None
        assert serialized["active"] == test_promotion.active

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
        assert serialized["modified_when"] is None
        assert serialized["active"] == test_promotion.active

    def test_serialized_promotion_with_missing_fields(self):
        """It should deserialize a Promotion into a dict with some fields as None"""
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
            "active": True,
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
        assert result.active

    def test_deserialize_invalid_promotion(self):
        """It should throw an exception for any invalid formats"""
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
            "start_date": "abc123",
        }
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, invalid_json_type)
        self.assertRaises(
            DataValidationError, promotion.deserialize, invalid_json_scope
        )
        self.assertRaises(DataValidationError, promotion.deserialize, invalid_json_date)
        assert promotion.promotion_name is None
        assert promotion.promotion_description is None
        assert promotion.promotion_scope is None
        assert promotion.start_date is None

    def test_deserialize_with_errors(self):
        """It should raise a DataValidationError"""
        promotion_json = {"promotion_id": 123, "promotion_name": "abcPromotion"}
        promotion = Promotion()
        original_deserialize_with_default = Promotion.deserialize_with_default
        try:
            # Type Error
            def type_error_deserialize(key, data, default, deserializer=None):
                raise TypeError("Some bad type")

            Promotion.deserialize_with_default = type_error_deserialize
            self.assertRaises(
                DataValidationError, promotion.deserialize, promotion_json
            )

            # Attribute Error
            def attribute_error_deserialize(key, data, default, deserializer=None):
                raise AttributeError("Some bad attribute")

            promotion.deserialize_with_default = attribute_error_deserialize
            self.assertRaises(
                DataValidationError, promotion.deserialize, promotion_json
            )

        finally:
            Promotion.deserialize_with_default = original_deserialize_with_default

    def test_create_missing_data(self):
        """It should throw a validation error since required fields are empty"""
        test_promotion = Promotion()
        test_promotion.name = "Name"

        self.assertRaises(DataValidationError, test_promotion.create)

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
        """It should not update promotion and raise DataValidationError"""
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

    def test_read_by_name(self):
        """It should get only promotions which have the name provided"""
        test_promotion = PromotionFactory()
        test_promotion.promotion_name = "abcde_Promotion"
        test_promotion.create()
        test_promotion_2 = PromotionFactory()
        test_promotion_2.promotion_name = "abcde_Promotion 2"
        test_promotion_2.create()
        db.session.expire_all()
        found_promotion = Promotion.find_by_name(test_promotion.promotion_name).all()
        self.assertEqual(len(found_promotion), 1)

    def test_find_by_date(self):
        """It should return all promotions valid on a specific date"""
        promotion1 = PromotionFactory()
        promotion1.start_date = datetime(2025, 1, 1)
        promotion1.end_date = datetime(2026, 1, 1)

        promotion2 = PromotionFactory()
        promotion2.start_date = datetime(2024, 1, 1)
        promotion2.end_date = datetime(2025, 3, 1)

        promotion3 = PromotionFactory()
        promotion3.start_date = datetime(2025, 1, 1)
        promotion3.end_date = datetime(2025, 6, 1)
        promotion1.create()
        promotion2.create()
        promotion3.create()
        results = Promotion.filter_by_datetime(
            datetime(2025, 6, 1), query=db.session.query(Promotion)
        ).all()
        self.assertEqual(len(results), 2)

    def test_find_by_scope(self):
        """It should return all promotions with the indicated scopes"""
        promotion1 = PromotionFactory()
        promotion1.promotion_scope = PromotionScope.PRODUCT_ID
        promotion1.create()

        promotion2 = PromotionFactory()
        promotion2.promotion_scope = PromotionScope.ENTIRE_STORE
        promotion2.create()

        promotion3 = PromotionFactory()
        promotion3.promotion_scope = PromotionScope.PRODUCT_CATEGORY
        promotion3.create()

        results = Promotion.filter_by_promotion_scope(
            [PromotionScope.ENTIRE_STORE, PromotionScope.PRODUCT_CATEGORY],
            query=db.session.query(Promotion),
        ).all()
        self.assertEqual(len(results), 2)

    def test_find_by_type(self):
        """It should return all promotions with the indicated types"""
        promotion1 = PromotionFactory()
        promotion1.promotion_type = PromotionType.ABSOLUTE
        promotion1.create()

        promotion2 = PromotionFactory()
        promotion2.promotion_type = PromotionType.ABSOLUTE
        promotion2.create()

        promotion3 = PromotionFactory()
        promotion3.promotion_type = PromotionType.PERCENTAGE
        promotion3.create()

        results = Promotion.filter_by_promotion_type(
            [PromotionType.ABSOLUTE], query=db.session.query(Promotion)
        ).all()
        self.assertEqual(len(results), 2)

    def test_find_by_filters(self):
        """It should return all promotions which match the required filters"""
        # Promotion meets criteria
        promotion1 = PromotionFactory()
        promotion1.start_date = datetime(2025, 1, 1)
        promotion1.end_date = datetime(2026, 1, 1)
        promotion1.promotion_scope = PromotionScope.ENTIRE_STORE
        promotion1.create()
        # Promotion meets scope criteria but not date criteria
        promotion2 = PromotionFactory()
        promotion2.start_date = datetime(2024, 1, 1)
        promotion2.end_date = datetime(2025, 3, 1)
        promotion2.promotion_scope = PromotionScope.ENTIRE_STORE
        promotion2.create()
        # Promotion meets date criteria but not scope criteria
        promotion3 = PromotionFactory()
        promotion3.start_date = datetime(2025, 1, 1)
        promotion3.end_date = datetime(2026, 1, 1)
        promotion3.promotion_scope = PromotionScope.PRODUCT_CATEGORY
        promotion3.create()
        # Promotion meets date criteria and second scope criteria
        promotion4 = PromotionFactory()
        promotion4.start_date = datetime(2025, 1, 1)
        promotion4.end_date = datetime(2026, 1, 1)
        promotion4.promotion_scope = PromotionScope.PRODUCT_ID
        promotion4.promotion_type = PromotionType.PERCENTAGE
        promotion4.create()

        test_filters = {
            "datetime": "2025-06-01",
            "promotion_scope": ["ENTIRE_STORE", "PRODUCT_ID"],
        }
        results = Promotion.find_with_filters(test_filters).all()
        result_ids = [result.promotion_id for result in results]

        self.assertEqual(len(results), 2)
        self.assertIn(promotion1.promotion_id, result_ids)
        self.assertIn(promotion4.promotion_id, result_ids)

        test_filters2 = {"promotion_type": ["ABSOLUTE"]}
        results2 = Promotion.find_with_filters(test_filters2).all()
        result_ids2 = [result.promotion_id for result in results2]
        self.assertEqual(len(results2), 3)
        self.assertNotIn(promotion4.promotion_id, result_ids2)
