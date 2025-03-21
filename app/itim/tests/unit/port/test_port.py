import pytest
import unittest

from django.test import TestCase

from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel

from itim.models.services import Port



@pytest.mark.django_db
class PortModel(
    TestCase,
    TenancyModel
):

    model = Port

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.item = self.model.objects.create(
            organization = self.organization,
            number = 1,
        )

        self.second_item = self.model.objects.create(
            organization = self.organization,
            number = 2,
        )

    @pytest.mark.skip(reason = 'to be written')
    def test_field_entry_invalid_port_to_high(self):
        """Test Model Field

        Ensure that a validation error is thrown and that is displays to the user
        """
        pass