import pytest

from django.test import TestCase

from access.models.company_base import Company
from access.tests.unit.entity.test_unit_entity_viewset import (
    EntityViewsetInheritedCases
)



@pytest.mark.model_company
class ViewsetTestCases(
    EntityViewsetInheritedCases,
):

    model: str = Company



class CompanyViewsetInheritedCases(
    ViewsetTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Company
    """

    model: str = None
    """name of the model to test"""



@pytest.mark.module_access
class CompanyViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    pass
