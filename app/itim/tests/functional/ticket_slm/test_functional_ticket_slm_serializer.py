import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_serializer import TicketBaseSerializerInheritedCases



@pytest.mark.model_slmticket
class SLMTicketSerializerTestCases(
    TicketBaseSerializerInheritedCases,
):

    parameterized_test_data: dict = {
        "tto": {
            'will_create': True,
            'permission_import_required': False,
        },
        "ttr": {
            'will_create': True,
            'permission_import_required': False,
        },
    }

    valid_data: dict = {
        'tto': 2,
        'ttr': 3,
    }



class SLMTicketSerializerInheritedCases(
    SLMTicketSerializerTestCases,
):

    model = None
    """Model to test"""

    parameterized_test_data: dict = None

    valid_data: dict = None
    """Valid data used by serializer to create object"""



@pytest.mark.module_itim
class SLMTicketSerializerPyTest(
    SLMTicketSerializerTestCases,
):

    parameterized_test_data: dict = None
