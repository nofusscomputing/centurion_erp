from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itam.models.device_type_notes import DeviceTypeNotes



class DeviceTypeNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = DeviceTypeNotes
