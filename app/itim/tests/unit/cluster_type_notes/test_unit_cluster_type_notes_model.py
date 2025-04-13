from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from itim.models.cluster_type_notes import ClusterTypeNotes



class ClusterTypeNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ClusterTypeNotes
