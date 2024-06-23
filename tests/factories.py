"""
Test Factory to make fake objects for testing
"""

import factory
import factory.random
import uuid
import datetime
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
    start_date = "2025-01-01"
    end_date = "2026-01-01"
    promotion_value = 50
    promotion_code = None
    created_by = uuid.uuid4()
    modified_by = uuid.uuid4()
    created_when = "2024-01-01"
    modified_when = None


    # Todo: Add your other attributes here...
