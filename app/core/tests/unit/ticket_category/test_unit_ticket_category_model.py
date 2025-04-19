from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from core.models.ticket.ticket_category import TicketCategory


class TicketCategoryModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = TicketCategory
