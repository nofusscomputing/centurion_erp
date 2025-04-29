from django.contrib.auth.models import User
from django.test import TestCase

from access.models.organization import Organization
from core.serializers.ticket import (
    TicketBase,
    ModelSerializer
)



class SerializerTestCases:

    model = TicketBase
    """Model to test"""

    create_model_serializer = ModelSerializer
    """Serializer to test"""

    valid_data: dict = {
        'title': 'title 2',
        'description': 'description',
    }
    """Valid data used by serializer to create object"""


    @classmethod
    def setUpTestData(self):
        """Setup Test"""
        
        self.organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.valid_data.update({
            'organization': self.organization.pk,
            'opened_by': self.user.pk,
        })

        self.item = self.model.objects.create(
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



class TicketBaseSerializerInheritedCases(
    SerializerTestCases,
):

    create_model_serializer = None
    """Serializer to test"""

    model = None
    """Model to test"""

    valid_data: dict = {}
    """Valid data used by serializer to create object"""


    @classmethod
    def setUpTestData(self):

        self.valid_data = {
            **super().valid_data,
            **self.valid_data
        }

        super().setUpTestData()



class TicketBaseSerializerTest(
    SerializerTestCases,
    TestCase,
):

    pass
