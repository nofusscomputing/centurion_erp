from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itam.models.device_model_notes import DeviceModelNotes



class DeviceModelNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = DeviceModelNotes
