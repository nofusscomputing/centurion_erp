import pytest

from itim.tests.functional.ticket_slm.test_functional_ticket_slm_serializer import SLMTicketSerializerInheritedCases



@pytest.mark.model_requestticket
class RequestTicketSerializerTestCases(
    SLMTicketSerializerInheritedCases,
):

    pass



class RequestTicketSerializerInheritedCases(
    RequestTicketSerializerTestCases,
):

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""



@pytest.mark.module_itim
class RequestTicketSerializerPyTest(
    RequestTicketSerializerTestCases,
):

    pass
