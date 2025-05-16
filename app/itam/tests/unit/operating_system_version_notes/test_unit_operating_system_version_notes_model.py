from django.test import TestCase

from access.models.tenant import Tenant as Organization

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itam.models.operating_system import OperatingSystem
from itam.models.operating_system_version_notes import OperatingSystemVersionNotes



class OperatingSystemVersionNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = OperatingSystemVersionNotes


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        self.kwargs_create_related_model: dict = {
            'organization': self.organization,
            'name': 'note model existing item',
            'operating_system': OperatingSystem.objects.create(
                organization = self.organization,
                name = 'os'
            )
        }

        super().setUpTestData()
