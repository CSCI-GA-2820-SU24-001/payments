"""
Test cases for Pet Model
"""

import os
import logging
from datetime import datetime
from unittest import TestCase
import uuid

from sqlalchemy import DateTime
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
    def test_create_promotion(self):
        promotion_id = 123
        promotion_name = "some_promotion"
        promotion_description = "a good promotion"
        promotion_type = PromotionType.ABSOLUTE
        promotion_scope = PromotionScope.PRODUCT_ID
        start_date = "2025-01-01"
        end_date = "2026-01-01"
        promotion_value = 50
        promotion_code = None
        created_by = uuid.uuid4()
        modified_by = uuid.uuid4()
        created_when = "2024-01-01"
        modified_when = None

        test_promotion = Promotion(promotion_id=promotion_id, promotion_name=promotion_name, 
                                   promotion_description=promotion_description, promotion_type=promotion_type,
                                   promotion_scope=promotion_scope, start_date=start_date, end_date=end_date,
                                   promotion_value=promotion_value, promotion_code=promotion_code,
                                   created_by=created_by, modified_by=modified_by,
                                   created_when=created_when, modified_when=modified_when)
        
        test_promotion.create()
        assert test_promotion.promotion_name == "some_promotion"
        assert test_promotion.created_by == created_by
        found = Promotion.all()
        self.assertEqual(len(found), 1)
        data = Promotion.find(test_promotion.promotion_id)
        self.assertEqual(data.promotion_name, test_promotion.promotion_name)
        self.assertEqual(data.start_date, datetime(2025, 1, 1, 0, 0))

    def test_create_promotions_instance(self):
        """It should create a YourResourceModel"""
        # Todo: Remove this test case example
        resource = Promotion()
        resource.create()
        self.assertIsNotNone(resource.promotion_id)
        found = Promotion.all()
        self.assertEqual(len(found), 1)
        data = Promotion.find(resource.promotion_id)
        self.assertEqual(data.promotion_name, resource.promotion_name)

        