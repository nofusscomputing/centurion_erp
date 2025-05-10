from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_api_fields import (
    TicketCommentBaseAPIInheritedCases
)



class TicketCommentSolutionAPITestCases(
    TicketCommentBaseAPIInheritedCases,
):

    parameterized_test_data = {}

    kwargs_create_item: dict = {}



class TicketCommentSolutionAPIInheritedCases(
    TicketCommentSolutionAPITestCases,
):

    kwargs_create_item: dict = {None}

    model = None



class TicketCommentSolutionAPIPyTest(
    TicketCommentSolutionAPITestCases,
):

    pass
