from django.test import TestCase

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from core.models.ticket.ticket_category_notes import TicketCategoryNotes



class NotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = TicketCategoryNotes
