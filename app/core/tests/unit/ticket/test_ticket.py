import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import TenancyModel

from core.models.ticket.ticket import Ticket


class TicketModel(
    TestCase,
    TenancyModel
):

    model = Ticket

    should_model_history_be_saved: bool = False
    """Tickets should not save model history.

    Saving of model history is not required as a ticket stores it's
    history as an 'action comment'
    """
