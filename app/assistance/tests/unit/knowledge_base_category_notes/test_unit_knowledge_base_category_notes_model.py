from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from assistance.models.knowledge_base_category_notes import KnowledgeCategoryBaseNotes



class KnowledgeCategoryBaseNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = KnowledgeCategoryBaseNotes
