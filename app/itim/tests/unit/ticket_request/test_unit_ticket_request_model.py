from itim.models.request_ticket import RequestTicket
from itim.tests.unit.ticket_slm.test_unit_ticket_slm_model import SLMTicketModelInheritedCases



class RequestTicketModelTestCases(
    SLMTicketModelInheritedCases,
):

    kwargs_create_item: dict = {}

    sub_model_type = 'request'


    def test_class_inherits_requestticket(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, RequestTicket)


    def test_function_get_ticket_type(self):
        """Function test

        As this model is intended to be used alone.

        Ensure that function `get_ticket_type` returns `request` for model
        `RequestTicket`
        """

        assert self.model().get_ticket_type == 'request'



class RequestTicketModelInheritedCases(
    RequestTicketModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model RequestTicket
    """

    kwargs_create_item: dict = None

    model = None

    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """


class RequestTicketModelPyTest(
    RequestTicketModelTestCases,
):

    pass
