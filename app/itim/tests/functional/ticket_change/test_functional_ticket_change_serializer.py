import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_serializer import TicketBaseSerializerInheritedCases



@pytest.mark.model_changeticket
class ChangeTicketSerializerTestCases(
    TicketBaseSerializerInheritedCases,
):

    parameterized_test_data: dict = {}

    valid_data: dict = {}



class ChangeTicketSerializerInheritedCases(
    ChangeTicketSerializerTestCases,
):

    model = None
    """Model to test"""

    parameterized_test_data: dict = None

    valid_data: dict = None
    """Valid data used by serializer to create object"""



@pytest.mark.module_itim
class ChangeTicketSerializerPyTest(
    ChangeTicketSerializerTestCases,
):

    parameterized_test_data: dict = None
