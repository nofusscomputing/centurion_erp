from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetBase, TicketViewSetPermissionsAPI, TicketViewSet



class ViewSetBase( TicketViewSetBase ):

    ticket_type = 'project_task'

    ticket_type_enum = Ticket.TicketType.PROJECT_TASK



class TicketProjectTaskPermissionsAPI(
    ViewSetBase,
    TicketViewSetPermissionsAPI,
    TestCase,
):

    pass



class TicketProjectTaskViewSet(
    TicketViewSet,
    ViewSetBase,
    TestCase,
):

    pass
