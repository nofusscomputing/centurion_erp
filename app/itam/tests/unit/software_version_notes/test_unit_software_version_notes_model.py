
from django.test import TestCase

from access.models.tenant import Tenant as Organization

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itam.models.software import Software
from itam.models.software_version_notes import SoftwareVersionNotes



class SoftwareVersionNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = SoftwareVersionNotes


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        self.kwargs_create_related_model: dict = {
            'organization': self.organization,
            'name': '11',
            'software': Software.objects.create(
                organization = self.organization,
                name = 'soft',
            )
        }

        super().setUpTestData()
