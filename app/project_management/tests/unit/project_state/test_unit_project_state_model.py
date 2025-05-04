from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from project_management.models.project_states import ProjectState


class ProjectStateModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = ProjectState
