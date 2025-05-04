from django.db.models.fields import NOT_PROVIDED
from django.test import TestCase

from access.tests.unit.contact.test_unit_contact_model import (
    Contact,
    ContactModelInheritedCases
)

from human_resources.models.employee import Employee



class ModelTestCases(
    ContactModelInheritedCases,
):

    model = Employee

    kwargs_item_create: dict = {
        'email': 'ipweird@unit.test',
        'employee_number': 123456,
    }



    def test_model_field_employee_number_mandatory(self):
        """Test Field

        Field `employee_number` must be a mandatory field
        """

        assert(
            not (
                self.model._meta.get_field('employee_number').blank
                and self.model._meta.get_field('employee_number').null
            )
            and self.model._meta.get_field('employee_number').default is NOT_PROVIDED
        )


    def test_model_inherits_contact(self):
        """Test model inheritence

        model must inherit from Entity sub-model `Contact`
        """

        assert issubclass(self.model, Contact)




class EmployeeModelInheritedCases(
    ModelTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Employee
    """

    kwargs_item_create: dict = None

    model = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create.update(
            super().kwargs_item_create
        )

        super().setUpTestData()



class EmployeeModelTest(
    ModelTestCases,
    TestCase,
):

    pass
