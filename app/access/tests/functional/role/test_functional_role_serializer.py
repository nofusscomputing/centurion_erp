import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError


from access.models.tenant import Tenant as Organization
from access.serializers.role import Role, ModelSerializer



@pytest.mark.model_role
@pytest.mark.model_role
class ValidationSerializer(
    TestCase,
):

    model = Role

    serializer = ModelSerializer


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.diff_organization = Organization.objects.create(name='test_org_diff_org')


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        self.valid_data = {
            'organization': self.organization.id,
            'name': 'two',
            'model_notes': 'dfsdfsd',
        }



    def test_serializer_validation_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        serializer = self.serializer(
            data = self.valid_data
        )


        assert serializer.is_valid( raise_exception = True )


    def test_serializer_validation_no_name_exception(self):
        """Serializer Validation Check

        Ensure that when creating and field name is not provided a
        validation error occurs
        """

        valid_data = self.valid_data.copy()

        del valid_data['name']

        with pytest.raises(ValidationError) as err:

            serializer = self.serializer(
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'
