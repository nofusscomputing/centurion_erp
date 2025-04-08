from django.test import TestCase

from access.models.person import Person
from access.tests.unit.entity.test_unit_entity_history_api_v2 import (
    EntityModelHistoryAPIInheritedCases
)



class PersonModelHistoryAPITestCases(
    EntityModelHistoryAPIInheritedCases,
):
    """ Model Histoy Test Cases

    Test must be setup by creating object `kwargs_create_audit_object` with the
    attributes required to create the object.
    """

    audit_model = None

    kwargs_create_audit_object: dict = None



class PersonHistoryAPIInheritedCases(
    PersonModelHistoryAPITestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Person
    """

    audit_model = None

    kwargs_create_audit_object: dict = None



class PersonModelHistoryAPITest(
    PersonModelHistoryAPITestCases,
    TestCase,
):

    audit_model = Person

    kwargs_create_audit_object: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }
