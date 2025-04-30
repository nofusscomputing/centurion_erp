from itim.tests.functional.ticket_slm.test_functional_ticket_slm_serializer import SLMTicketSerializerInheritedCases



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



class RequestTicketSerializerPyTest(
    RequestTicketSerializerTestCases,
):

    pass
