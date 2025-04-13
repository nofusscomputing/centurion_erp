from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from project_management.models.project_type_notes import ProjectTypeNotes



class ProjectTypeNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ProjectTypeNotes
