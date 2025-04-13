from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itam.models.software_notes import SoftwareNotes



class SoftwareNotesModel(
        ModelNotesInheritedCases
,
    TestCase,
):

    model = SoftwareNotes
