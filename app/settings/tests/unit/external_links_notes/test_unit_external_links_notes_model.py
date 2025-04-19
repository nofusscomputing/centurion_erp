from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from settings.models.external_link_notes import ExternalLinkNotes



class ExternalLinkNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ExternalLinkNotes
