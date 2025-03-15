import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models.organization import Organization

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag
from devops.serializers.public_feature_flag import FeatureFlag, ViewSerializer

from itam.models.software import Software



class Serializer(
    TestCase,
):

    model = FeatureFlag

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.diff_organization = Organization.objects.create(name='test_org_diff_org')

        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            software = software,
            description = 'desc',
            model_notes = 'text',
            enabled = True
        )

        self.valid_data = {
            'organization': self.organization.id,
            'name': 'two',
            'software': software.id,
            'description': 'a description',
            'model_notes': 'dfsdfsd',
            'enabled': True
        }


        self.software_no_feature_flag_enabled = Software.objects.create(
            organization = self.organization,
            name = 'soft no flagging',
        )



    def test_serializer_validation_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        serializer = ViewSerializer(
            data = self.valid_data
        )


        assert serializer.is_valid( raise_exception = True )
