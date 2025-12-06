from typing import Any


import pytest

from django.apps import apps

from core.models.ticket_comment_task import TicketCommentTask
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_viewset import (
    TicketCommentBaseViewsetInheritedCases,
    TicketBase
)



@pytest.mark.model_ticketcommenttask
class ViewsetTestCases(
    TicketCommentBaseViewsetInheritedCases,
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model': {
                'value': TicketCommentTask
            },
        }



    @staticmethod
    def all_ticket_types() -> list:

        ticket_models = []

        for ticket_model in apps.get_models():

            if not issubclass(ticket_model, TicketBase):
                continue

            ticket_models += [ ticket_model ]

        
        return ticket_models



    @pytest.mark.parametrize(
        argnames='ticket_model', 
        argvalues=[ticket_model for ticket_model in all_ticket_types()], 
        ids=[ticket_model._meta.model_name for ticket_model in all_ticket_types()]
    )
    def test_perm_map_task_comment_adds_triage(self, request, viewset, mocker,
        ticket_model
    ):

        view_set = viewset()

        mocker.patch.object(view_set, 'parent_model', ticket_model)


        ticket_model = request.getfixturevalue(
            f'model_{ticket_model._meta.model_name}'
        )

        ticket_model_kwargs = request.getfixturevalue(
            f'kwargs_{ticket_model._meta.model_name}'
        )()

        ticket = ticket_model.objects.create( **ticket_model_kwargs )


        view_set.kwargs = {
            'ticket_comment_model': 'task',
            'ticket_id': ticket.id
        }


        triage_permission = f'{ticket_model._meta.app_label}.triage_{ticket_model._meta.model_name}'

        expected = {
            'POST': [ triage_permission ],
            'PUT': [ triage_permission ],
            'PATCH': [ triage_permission ],
            'DELETE': [ triage_permission ],
        }

        assert view_set.perms_map == expected





class TicketCommentTaskViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentTaskViewsetPyTest(
    ViewsetTestCases,
):

    pass
