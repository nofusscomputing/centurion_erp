import pytest

from django.test import TestCase

from access.models.organization import Organization
from access.serializers.entity import (
    Entity,
    ModelSerializer
)



class SerializerTestCases:

    kwargs_create_item: dict = {}
    """ Model kwargs to create item"""

    model = Entity
    """Model to test"""

    create_model_serializer = ModelSerializer
    """Serializer to test"""

    valid_data: dict = {}
    """Valid data used by serializer to create object"""


    @classmethod
    def setUpTestData(self):
        """Setup Test"""
        
        self.organization = Organization.objects.create(name='test_org')

        self.kwargs_create_item.update({
            'model_notes': 'model notes field'
        })

        self.valid_data.update({
            'organization': self.organization.pk,
            'model_notes': 'model notes field'
        })

        self.item = self.model.objects.create(
            organization = self.organization,
            **self.kwargs_create_item,
        )



    def test_serializer_valid_data(self):
        """Serializer Validation Check

        Ensure that when creating an object with valid data, no validation
        error occurs.
        """

        serializer = self.create_model_serializer(
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_model_notes(self):
        """Serializer Validation Check

        Ensure that if creating and no model_notes is provided no validation
        error occurs
        """

        data = self.valid_data.copy()
        
        del data['model_notes']

        serializer = self.create_model_serializer(
            data = data
        )

        assert serializer.is_valid(raise_exception = True)



class EntitySerializerInheritedCases(
    SerializerTestCases,
):

    create_model_serializer = None
    """Serializer to test"""

    kwargs_create_item: dict = None
    """ Model kwargs to create item"""

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""



class EntitySerializerTest(
    SerializerTestCases,
    TestCase,
):

    pass
