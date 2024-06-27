"""
Models for YourResourceModel

All of the models are stored in this module
"""

import logging
import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class PromotionType(enum.Enum):
    """Used to represent different types of promotions"""

    PERCENTAGE = 1
    ABSOLUTE = 2

    @classmethod
    def deserialize(cls, promotion_type_str: str):
        """ Convert promotion_type_str into a PromotionType or None"""
        if promotion_type_str is None:
            return None
        try:
            return PromotionType[promotion_type_str]
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
        if promotion_scope_str is None:
            return None
        try:
            return PromotionScope[promotion_scope_str]
        except KeyError as error:
            raise DataValidationError(
                f"Error: '{promotion_scope_str}' is not a valid PromotionType"
            ) from error


class Promotion(db.Model):
    """
    Class that represents a YourResourceModel
    """

    ##################################################
    # Table Schema
    ##################################################
    promotion_id = db.Column(db.Integer, primary_key=True)
    promotion_name = db.Column(db.String(63))
    promotion_description = db.Column(db.String(255))
    promotion_type = db.Column(db.Enum(PromotionType))
    promotion_scope = db.Column(db.Enum(PromotionScope))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    promotion_value = db.Column(db.Double)
    promotion_code = db.Column(db.String(63), nullable=True)
    created_by = db.Column(db.Uuid)
    modified_by = db.Column(db.Uuid, nullable=True)
    created_when = db.Column(db.DateTime)
    modified_when = db.Column(db.DateTime)

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
            "promotion_type": self.promotion_type,
            "promotion_scope": self.promotion_scope,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "promotion_value": self.promotion_value,
            "promotion_code": self.promotion_code,
            "created_by": self.created_by,
            "modified_by": self.modified_by,
            "created_when": self.created_when,
            "modified_when": self.modified_when,
        }

    def deserialize_datetime(self, datetime_str: str):
        """
        Deserialize a datetime from a datetime string
        Args:
            datetime_str: A string representing the date or None
        """
        if datetime_str is None:
            return None
        try:
            formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']
            for fmt in formats:
                try:
                    return datetime.strptime(datetime_str, fmt)
                except ValueError:
                    continue
            raise ValueError(
                f"Time data '{datetime_str}' does not match any of the expected formats."
            )
        except ValueError as error:
            raise DataValidationError(
                f"Invalid date format: {datetime_str} does not conform to any valid datetime format"
            ) from error

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary
        Args:
            data (dict): A dictionary containing the promotion data
        """
        try:
            self.promotion_id = data.get("promotion_id", None)
            self.promotion_name = data.get("promotion_name", None)
            self.promotion_description = data.get("promotion_description", None)
            self.promotion_type = PromotionType.deserialize(data.get("promotion_type", None))
            self.promotion_scope = PromotionScope.deserialize(
                data.get("promotion_scope", None)
            )
            self.start_date = self.deserialize_datetime(data.get("start_date", None))
            self.end_date = self.deserialize_datetime(data.get("end_date", None))
            self.promotion_value = data.get("promotion_value", None)
            self.promotion_code = data.get("promotion_code", None)
            self.created_by = data.get("created_by", None)
            self.modified_by = data.get("modified_by", None)
            self.created_when = self.deserialize_datetime(data.get("created_when", None))
            self.modified_when = self.deserialize_datetime(data.get(
                "modified_when", None
            ))
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: missing " + error.args[0]
            ) from error
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
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
