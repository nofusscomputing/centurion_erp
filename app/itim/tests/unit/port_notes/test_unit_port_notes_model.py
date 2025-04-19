from django.test import TestCase

from access.models.organization import Organization

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itim.models.port_notes import PortNotes



class PortNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    

    model = PortNotes


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        self.kwargs_create_related_model: dict = {
            'organization': self.organization,
            'number': 22,
        }

        super().setUpTestData()
