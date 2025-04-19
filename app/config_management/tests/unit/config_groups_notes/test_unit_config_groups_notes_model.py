from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from config_management.models.config_group_notes import ConfigGroupNotes



class ConfigGroupNotesNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ConfigGroupNotes
