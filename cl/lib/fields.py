from django.db import models
from django_elasticsearch_dsl import fields
from elasticsearch_dsl import Join, Percolator


class CharNullField(models.CharField):
    """
    Subclass of the CharField that allows empty strings to be stored as NULL.

    https://stackoverflow.com/a/1934764/64911
    """

    description = "CharField that stores NULL but returns ''."

    def from_db_value(self, value, expression, connection):
        """
        Gets value right out of the db and changes it if its ``None``.
        """
        return "" if value is None else value

    def to_python(self, value):
        """
        Gets value right out of the db or an instance, and changes it if its ``None``.
        """
        if isinstance(value, models.CharField):
            # If an instance, just return the instance.
            return value
        return "" if value is None else value

    def get_prep_value(self, value):
        """
        Catches value right before sending to db.
        """
        return None if value == "" else value


class PercolatorField(fields.DEDField, Percolator):
    """Subclass of DEDField and Percolator field.
    This subclass transforms the Percolator field into a field compatible with
    django_elasticsearch_dsl. This enables us to leverage DED Document methods
    like "prepare," which allows the field to be populated using the prepare
    method.
    """

    pass


class JoinField(fields.DEDField, Join):
    """Subclass of DEDField and Join field.
    This subclass transforms the Join field into a field compatible with
    django_elasticsearch_dsl. This enables us to leverage DED Document methods
    like "prepare," which allows the field to be populated using the prepare
    method.
    """

    pass
