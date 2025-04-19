from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itim.models.service_notes import ServiceNotes



class ServiceNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ServiceNotes
