import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelCommon



class ProjectMilestoneViews(
    TestCase,
    ModelCommon
):

    add_module = 'project_management.views.project_milestones'
    add_view = 'Add'

    change_module = add_module
    change_view = 'Change'

    delete_module = add_module
    delete_view = 'Delete'

    display_module = add_module
    display_view = 'View'

    # index_module = add_module
    # index_view = 'Index'
