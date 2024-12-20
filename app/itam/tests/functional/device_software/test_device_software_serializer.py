import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from itam.serializers.device_software import Device, DeviceSoftware, DeviceSoftwareModelSerializer
from itam.models.software import Software, SoftwareCategory, SoftwareVersion



class MockView:

    action: str = None

    kwargs: dict = {}



class DeviceInstallsValidationAPI(
    TestCase,
):

    model = DeviceSoftware

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.software_category = SoftwareCategory.objects.create(
            organization=organization,
            name = 'category'
        )

        self.software = Software.objects.create(
            organization=organization,
            name = 'software',
            category = self.software_category
        )

        self.software_version = SoftwareVersion.objects.create(
            organization=organization,
            name = '12',
            software = self.software
        )

        self.device = Device.objects.create(
            organization=organization,
            name = 'device'
        )


        self.item = self.model.objects.create(
            organization=self.organization,
            software = self.software,
            version = self.software_version,
            device = self.device
        )

        self.valid_data: dict = {
            'organization': self.organization.pk,
            'software': self.software.pk,
            'version': self.software_version.pk,
            'device': self.device.pk
        }



    def test_serializer_validation_create(self):
        """Serializer Validation Check

        Ensure that an item can be created
        """


        mock_view = MockView()

        mock_view.kwargs = {
            'device_id': self.valid_data['device']
        }

        data = self.valid_data.copy()


        serializer = DeviceSoftwareModelSerializer(
            context = {
                'view': mock_view
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_device(self):
        """Serializer Validation Check

        Ensure that if creating and no device is provided no validation error
        occurs as the serializer provides the device from the view.
        """

        mock_view = MockView()

        mock_view.kwargs = {
            'device_id': self.valid_data['device']
        }

        data = self.valid_data.copy()

        del data['device']

        serializer = DeviceSoftwareModelSerializer(
            context = {
                'view': mock_view
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_software(self):
        """Serializer Validation Check

        Ensure that if creating and no device is provided a validation exception is thrown
        """

        mock_view = MockView()

        mock_view.kwargs = {
            'device_id': self.valid_data['device']
        }

        data = self.valid_data.copy()

        del data['software']

        with pytest.raises(ValidationError) as err:

            serializer = DeviceSoftwareModelSerializer(
                context = {
                    'view': mock_view
                },
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['software'][0] == 'required'
