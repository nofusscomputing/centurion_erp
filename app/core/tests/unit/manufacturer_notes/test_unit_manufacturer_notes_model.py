from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from core.models.manufacturer_notes import ManufacturerNotes



class ManufacturerNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ManufacturerNotes
