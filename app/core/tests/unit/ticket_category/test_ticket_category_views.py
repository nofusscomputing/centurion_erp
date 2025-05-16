import pytest
import unittest
import requests

from django.test import TestCase

from centurion.tests.abstract.models import PrimaryModel, ModelAdd, ModelChange, ModelDelete



# class TicketCommentViews(
#     TestCase,
#     PrimaryModel
# ):
class TicketCategoryViews(
    TestCase,
    PrimaryModel
):

    add_module = 'core.views.ticket_categories'
    add_view = 'Add'

    change_module = add_module
    change_view = 'Change'

    delete_module = add_module
    delete_view = 'Delete'

    display_module = add_module
    display_view = 'View'

    index_module = add_module
    index_view = 'Index'
