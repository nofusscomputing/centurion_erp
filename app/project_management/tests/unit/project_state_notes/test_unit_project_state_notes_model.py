from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from project_management.models.project_state_notes import ProjectStateNotes



class ProjectStateNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ProjectStateNotes
