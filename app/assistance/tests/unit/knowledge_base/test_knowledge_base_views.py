import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import PrimaryModel



class ConfigManagementViews(
    TestCase,
    PrimaryModel
):

    add_module = 'assistance.views.knowledge_base'
    add_view = 'Add'

    change_module = add_module
    change_view = 'Change'

    delete_module = add_module
    delete_view = 'Delete'

    display_module = add_module
    display_view = 'View'

    index_module = add_module
    index_view = 'Index'
