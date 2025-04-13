from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itam.models.operating_system_notes import OperatingSystemNotes



class OperatingSystemNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = OperatingSystemNotes
