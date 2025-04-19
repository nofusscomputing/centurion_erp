from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from access.models.team_notes import TeamNotes



class TeamNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    kwargs_create_related_model = {
        'team_name': 'team one'
    }

    model = TeamNotes
