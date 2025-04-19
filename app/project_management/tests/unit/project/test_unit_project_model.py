import pytest

from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from project_management.models.projects import Project


class ProjectModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = Project


    @pytest.mark.skip( reason = 'to be written')
    def test_attribute_duration_ticket_value(self):
        """Attribute value test

        This aattribute calculates the ticket duration from
        it's comments. must return total time in seconds
        """

        pass