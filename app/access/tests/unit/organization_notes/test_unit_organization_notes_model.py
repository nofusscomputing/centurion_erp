# from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from access.models.organization_notes import OrganizationNotes



class OrganizationNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = OrganizationNotes
