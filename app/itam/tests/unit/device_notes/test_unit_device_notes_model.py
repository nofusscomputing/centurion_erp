from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itam.models.device_notes import DeviceNotes



class DeviceNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = DeviceNotes
