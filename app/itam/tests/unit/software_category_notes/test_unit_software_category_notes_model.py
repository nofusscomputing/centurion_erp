from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itam.models.software_category_notes import SoftwareCategoryNotes



class SoftwareCategoryNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = SoftwareCategoryNotes
