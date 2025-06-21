from django.test import TestCase

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from core.models.ticket.ticket_comment_category import TicketCommentCategory


class TicketCommentCategoryModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = TicketCommentCategory
