import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models.tenant import Tenant as Organization

from app.tests.abstract.mock_view import MockView, User

from itam.serializers.software_version import Software, SoftwareVersion, SoftwareVersionModelSerializer



class SoftwareVersionValidationAPI(
    TestCase,
):

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.organization = organization

        self.software = Software.objects.create(
            organization=organization,
            name = 'os name',
        )

        self.mock_view = MockView( user = self.user )



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = SoftwareVersionModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                "organization": self.organization.id,
                "software": self.software.id
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'
