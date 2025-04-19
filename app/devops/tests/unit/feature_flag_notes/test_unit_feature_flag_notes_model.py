from django.test import TestCase

from access.models.organization import Organization

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from devops.models.feature_flag_notes import FeatureFlagNotes
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software



class FeatureFlagNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = FeatureFlagNotes


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')


        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )
        self.kwargs_create_related_model: dict = {
            'name': 'one',
            'software': software,
            'description': 'desc',
            'model_notes': 'text',
            'enabled': True
        }

        super().setUpTestData()



    def test_attribute_type_app_namespace(self):
        """Attribute Type

        app_namespace is of type str
        """

        assert type(self.model.app_namespace) is str


    def test_attribute_value_app_namespace(self):
        """Attribute Type

        app_namespace has been set, override this test case with the value
        of attribute `app_namespace`
        """

        assert self.model.app_namespace == 'devops'
