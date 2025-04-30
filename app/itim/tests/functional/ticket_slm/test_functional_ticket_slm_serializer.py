from core.tests.functional.ticket_base.test_functional_ticket_base_serializer import TicketBaseSerializerInheritedCases



class SLMTicketSerializerTestCases(
    TicketBaseSerializerInheritedCases,
):

    parametrized_test_data: dict = {
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

    parametrized_test_data: dict = None

    valid_data: dict = None
    """Valid data used by serializer to create object"""



class SLMTicketSerializerPyTest(
    SLMTicketSerializerTestCases,
):

    parametrized_test_data: dict = None

