from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from core.models.ticket.ticket_comment_category import TicketCommentCategory


class TicketCommentCategoryModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = TicketCommentCategory
