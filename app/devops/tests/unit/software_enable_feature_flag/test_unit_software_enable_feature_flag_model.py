from django.test import TestCase

from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software



class Model(
    TenancyModel,
    TestCase,
):

    model = SoftwareEnableFeatureFlag


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization


        self.item = self.model.objects.create(
            organization = self.organization,
            # name = 'one',
            software = Software.objects.create(
                organization = self.organization,
                name = 'soft',
            ),
            # description = 'desc',
            # model_notes = 'text',
            enabled = True
        )
