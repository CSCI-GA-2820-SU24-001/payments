"""
Test Factory to make fake objects for testing
"""

import factory
import factory.random
from service.models import Promotion


class PromotionFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    promotion_id = factory.Sequence(lambda n: n)
    promotion_name = factory.Faker("some_promotion")
    promotion_description = factory.Faker("some_description")
    promotion_type = factory.Faker("123")

    # Todo: Add your other attributes here...
