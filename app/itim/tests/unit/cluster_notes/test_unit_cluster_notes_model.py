from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itim.models.cluster_notes import ClusterNotes



class ClusterNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ClusterNotes
