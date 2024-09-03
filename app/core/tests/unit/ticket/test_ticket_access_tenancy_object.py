import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.tests.abstract.tenancy_object import TenancyObject

from core.models.ticket.ticket import Ticket



class TicketTenancyObject(
    TestCase,
    TenancyObject
):

    model = Ticket
