from django.test import TestCase

from access.models.company_base import Company
from access.tests.unit.entity.test_unit_entity_viewset import (
    EntityViewsetInheritedCases
)



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



class CompanyViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    pass
