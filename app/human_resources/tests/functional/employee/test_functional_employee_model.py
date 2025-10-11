import pytest

from access.tests.functional.contact.test_functional_contact_model import ContactModelInheritedCases



@pytest.mark.model_employee
class EmployeeModelTestCases(
    ContactModelInheritedCases
):
    pass



class EmployeeModelInheritedCases(
    EmployeeModelTestCases,
):
    pass



@pytest.mark.module_human_resources
class EmployeeModelPyTest(
    EmployeeModelTestCases,
):
    pass
