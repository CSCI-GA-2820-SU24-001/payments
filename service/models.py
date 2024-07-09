"""
Models for YourResourceModel

All of the models are stored in this module
"""

import logging
import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from service.common.datetime_utils import datetime_from_str, datetime_to_str

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy(session_options={"autoflush": False})


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class PromotionType(enum.Enum):
    """Used to represent different types of promotions"""

    PERCENTAGE = 1
    ABSOLUTE = 2

    @classmethod
    def deserialize(cls, promotion_type_str: str):
        """Convert promotion_type_str into a PromotionType or None"""
        try:
            return PromotionType[promotion_type_str.upper()]
        except KeyError as error:
            raise DataValidationError(
                f"Error: '{promotion_type_str}' is not a valid PromotionType"
            ) from error


class PromotionScope(enum.Enum):
    """Used to represent the scope a promotion is applicable to"""

    PRODUCT_ID = 1
    PRODUCT_CATEGORY = 2
    ENTIRE_STORE = 3

    @classmethod
    def deserialize(cls, promotion_scope_str: str):
        """Convert promotion_scope_str into a PromotionType or None"""
        try:
            return PromotionScope[promotion_scope_str.upper()]
        except KeyError as error:
            raise DataValidationError(
                f"Error: '{promotion_scope_str}' is not a valid PromotionType"
            ) from error


class Promotion(db.Model):  # pylint: disable=too-many-instance-attributes
    """
    Class that represents a YourResourceModel
    """

    ##################################################
    # Table Schema
    ##################################################
    promotion_id = db.Column(db.Integer, primary_key=True)
    promotion_name = db.Column(db.String(63), nullable=False)
    promotion_description = db.Column(db.String(255), nullable=False)
    promotion_type = db.Column(db.Enum(PromotionType), nullable=False)
    promotion_scope = db.Column(db.Enum(PromotionScope), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    promotion_value = db.Column(db.Double, nullable=False)
    promotion_code = db.Column(db.String(63), nullable=True)
    created_by = db.Column(db.Uuid, nullable=False)
    modified_by = db.Column(db.Uuid, nullable=True)
    created_when = db.Column(db.DateTime, nullable=False)
    modified_when = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Promotion {self.promotion_name} promotion_id=[{self.promotion_id}], promotion_name=[{self.promotion_name}]>"

    def create(self):
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s", self.promotion_name)
        self.promotion_id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.promotion_name)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a YourResourceModel from the data store"""
        logger.info("Deleting %s", self.promotion_name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a YourResourceModel into a dictionary"""
        return {
            "promotion_id": self.promotion_id,
            "promotion_name": self.promotion_name,
            "promotion_description": self.promotion_description,
            "promotion_type": self.promotion_type.name,
            "promotion_scope": self.promotion_scope.name,
            "start_date": datetime_to_str(self.start_date),
            "end_date": datetime_to_str(self.end_date),
            "promotion_value": self.promotion_value,
            "promotion_code": self.promotion_code,
            "created_by": self.created_by,
            "modified_by": self.modified_by,
            "created_when": datetime_to_str(self.created_when),
            "modified_when": (
                datetime_to_str(self.modified_when) if self.modified_when else None
            ),
        }

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary
        Args:
            data (dict): A dictionary containing the promotion data
        """
        try:
            updated_promotion = Promotion()
            updated_promotion.promotion_id = Promotion.deserialize_with_default(
                "promotion_id", data, self.promotion_id
            )
            updated_promotion.promotion_name = Promotion.deserialize_with_default(
                "promotion_name", data, self.promotion_name
            )
            updated_promotion.promotion_description = (
                Promotion.deserialize_with_default(
                    "promotion_description", data, self.promotion_description
                )
            )
            updated_promotion.promotion_type = Promotion.deserialize_with_default(
                "promotion_type", data, self.promotion_type, PromotionType.deserialize
            )
            updated_promotion.promotion_scope = Promotion.deserialize_with_default(
                "promotion_scope",
                data,
                self.promotion_scope,
                PromotionScope.deserialize,
            )
            updated_promotion.start_date = Promotion.deserialize_with_default(
                "start_date", data, self.start_date, Promotion.deserialize_datetime
            )
            updated_promotion.end_date = Promotion.deserialize_with_default(
                "end_date", data, self.end_date, Promotion.deserialize_datetime
            )
            updated_promotion.promotion_value = Promotion.deserialize_with_default(
                "promotion_value", data, self.promotion_value
            )
            updated_promotion.promotion_code = Promotion.deserialize_with_default(
                "promotion_code", data, self.promotion_code
            )
            updated_promotion.created_by = Promotion.deserialize_with_default(
                "created_by", data, self.created_by
            )
            updated_promotion.modified_by = Promotion.deserialize_with_default(
                "modified_by", data, self.modified_by
            )
            updated_promotion.created_when = Promotion.deserialize_with_default(
                "created_when", data, self.created_when, Promotion.deserialize_datetime
            )
            updated_promotion.modified_when = Promotion.deserialize_with_default(
                "modified_when",
                data,
                self.modified_when,
                Promotion.deserialize_datetime,
            )
            # Only update once all fields have been verified and deserialized
            self.promotion_id = updated_promotion.promotion_id
            self.promotion_name = updated_promotion.promotion_name
            self.promotion_description = updated_promotion.promotion_description
            self.promotion_type = updated_promotion.promotion_type
            self.promotion_scope = updated_promotion.promotion_scope
            self.start_date = updated_promotion.start_date
            self.end_date = updated_promotion.end_date
            self.promotion_value = updated_promotion.promotion_value
            self.promotion_code = updated_promotion.promotion_code
            self.created_by = updated_promotion.created_by
            self.modified_by = updated_promotion.modified_by
            self.created_when = updated_promotion.created_when
            self.modified_when = updated_promotion.modified_when

        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def deserialize_with_default(cls, key, data, default, deserializer=None):
        """Deserializes a field with a provided key from incoming json with a default value.
        Uses provided deserializer if provided

        Args:
            key (string): The string to extract from the data
            data (dict): The JSON object containing the incoming data
            default (Any): the default to use if no data is found
            deserializer (function, optional): Provided deserializer. Defaults to None.
        """
        if not data.get(key, None):
            return default
        if deserializer is not None:
            return deserializer(data.get(key))
        return data.get(key)

    @classmethod
    def deserialize_datetime(cls, datetime_str: str):
        """
        Deserialize a datetime from a datetime string
        Args:
            datetime_str: A string representing the date
        """
        try:
            return datetime_from_str(datetime_str)
        except ValueError as error:
            raise DataValidationError(
                f"Invalid date format: {datetime_str} does not conform to any valid datetime format"
            ) from error

    @classmethod
    def to_list_deserializer(cls, deserializer):
        """Converts a deserialization function to an equivalent one for a list of the specified object"""

        def deserialize_list(ls):
            return [deserializer(item) for item in ls]

        return deserialize_list

    @classmethod
    def all(cls):
        """Returns all of the YourResourceModels in the database"""
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a YourResourceModel by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_with_filters(cls, filters):
        """Finds all Promotions by applying filters from a dict"""
        datetime_filter = Promotion.deserialize_with_default(
            "datetime", filters, None, Promotion.deserialize_datetime
        )
        promotion_types_filter = Promotion.deserialize_with_default(
            "promotion_type",
            filters,
            None,
            Promotion.to_list_deserializer(PromotionType.deserialize),
        )
        promotion_scopes_filter = Promotion.deserialize_with_default(
            "promotion_scope",
            filters,
            None,
            Promotion.to_list_deserializer(PromotionScope.deserialize),
        )
        query = db.session.query(Promotion)
        if datetime_filter is not None:
            query = Promotion.filter_by_datetime(datetime_filter, query)
        if promotion_types_filter is not None:
            query = Promotion.filter_by_promotion_type(promotion_types_filter, query)
        if promotion_scopes_filter is not None:
            query = Promotion.filter_by_promotion_scope(promotion_scopes_filter, query)

        return query

    @classmethod
    def filter_by_datetime(cls, datetime, query):
        """Returns all promotions which are valid at the specified datetime

        Args:
            datetime (_type_): datetime where promotion should be valid
        """
        return query.filter(and_(cls.start_date <= datetime, cls.end_date >= datetime))

    @classmethod
    def filter_by_promotion_type(cls, promotion_types, query):
        """Returns all promotions which have the specified type

        Args:
            promotion_type (PromotionType): promotion type to match
        """
        return query.filter(cls.promotion_type.in_(promotion_types))

    @classmethod
    def filter_by_promotion_scope(cls, promotion_scopes, query):
        """Returns all promotions which have the specified scope

        Args:
            promotion_scope (PromotionScope): promotion scope to match
        """
        return query.filter(cls.promotion_scope.in_(promotion_scopes))

    @classmethod
    def find_by_name(cls, name):
        """Returns all Promotions with the given name

        Args:
            name (string): the name of the Promotions you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.promotion_name == name)
