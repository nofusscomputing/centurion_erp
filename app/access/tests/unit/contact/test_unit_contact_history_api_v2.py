from django.test import TestCase

from access.models.contact import Contact
from access.tests.unit.person.test_unit_person_history_api_v2 import (
    PersonHistoryAPIInheritedCases
)



class ContactModelHistoryAPITestCases(
    PersonHistoryAPIInheritedCases,
):
    """ Model Histoy Test Cases

    Test must be setup by creating object `kwargs_create_audit_object` with the
    attributes required to create the object.
    """

    audit_model = Contact

    kwargs_create_audit_object: dict = {
        'email': 'ipfunny@unit.test',
    }



class ContactHistoryAPIInheritedCases(
    ContactModelHistoryAPITestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Contact
    """

    audit_model = None

    kwargs_create_audit_object: dict = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_audit_object.update(
            super().kwargs_create_audit_object
        )

        super().setUpTestData()



class ContactModelHistoryAPITest(
    ContactModelHistoryAPITestCases,
    TestCase,
):

    pass
