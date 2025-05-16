from django.test import TestCase

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from project_management.models.project_types import ProjectType


class ProjectTypeModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = ProjectType
