from itim.tests.unit.ticket_slm.test_unit_ticket_slm_api_fields import TicketSLMAPIInheritedCases



class TicketRequestAPITestCases(
    TicketSLMAPIInheritedCases,
):

    model = None



class TicketRequestAPIInheritedCases(
    TicketRequestAPITestCases,
):

    kwargs_create_item: dict = None

    model = None



class TicketRequestAPIPyTest(
    TicketRequestAPITestCases,
):

    pass
