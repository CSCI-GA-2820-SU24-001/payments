"""
Test Factory to make fake objects for testing
"""
import uuid
import datetime

import factory
import factory.random
from service.models import Promotion, PromotionType, PromotionScope


class PromotionFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    promotion_name = "some_promotion"
    promotion_description = "a good promotion"
    promotion_type = PromotionType.ABSOLUTE
    promotion_scope = PromotionScope.PRODUCT_ID
    start_date = datetime.datetime(2025, 1, 1, 0, 0)
    end_date = datetime.datetime(2026, 1, 1, 0, 0)
    promotion_value = 50
    promotion_code = None
    created_by = uuid.uuid4()
    modified_by = uuid.uuid4()
    created_when = None
    modified_when = None
    active = False
