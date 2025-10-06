import pytest
import random

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_ticketbase
class APITestCases(
    APIFieldsInheritedCases,
):


    @pytest.fixture( scope = 'class')
    def create_model(self, request, django_db_blocker,
        model, model_kwargs, model_entity
    ):

        item = None

        with django_db_blocker.unblock():

            entity_user = model_entity.objects.create(
                organization = model_kwargs()['organization'],
                model_notes = 'asdas'
            )

            parent_ticket = model.objects.create(
                organization = model_kwargs()['organization'],
                title = 'parent ticket' + str(random.randint(9999,999999)),
                description = 'bla bla',
                opened_by = model_kwargs()['opened_by'],
            )


            kwargs = model_kwargs()
            kwargs['parent_ticket'] = parent_ticket

            kwargs['is_solved'] = True
            kwargs['date_solved'] = '2025-05-12T02:30:01Z'
            kwargs['is_closed'] = True
            kwargs['date_closed'] = '2025-05-12T02:30:02Z'
            kwargs['status'] = model.TicketStatus.CLOSED

            item = model.objects.create(
                **kwargs
            )


            item.assigned_to.add(entity_user)
            item.subscribed_to.add(entity_user)


            request.cls.item = item

        yield item

        with django_db_blocker.unblock():

            item.delete()

            parent_ticket.delete()

            entity_user.delete()



    @property
    def parameterized_api_fields(self):

        return {
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            '_urls.notes': {
                'expected': models.NOT_PROVIDED
            },
            'external_system': {
                'expected': int
            },
            'external_ref': {
                'expected': int
            },
            'parent_ticket': {
                'expected': dict
            },
            'parent_ticket.id': {
                'expected': int
            },
            'parent_ticket.display_name': {
                'expected': str
            },
            'parent_ticket.url': {
                'expected': str
            },
            'ticket_type': {
                'expected': str
            },
            'status': {
                'expected': int
            },
            'status_badge': {
                'expected': dict
            },
            'status_badge.icon': {
                'expected': dict
            },
            'status_badge.icon.name': {
                'expected': str
            },
            'status_badge.icon.style': {
                'expected': str
            },
            'status_badge.text': {
                'expected': str
            },
            'status_badge.text_style': {
                'expected': str
            },
            'status_badge.url': {
                'expected': type(None)
            },
            'category': {
                'expected': dict
            },
            'category.id': {
                'expected': int
            },
            'category.display_name': {
                'expected': str
            },
            'category.url': {
                'expected': Hyperlink
            },
            'title': {
                'expected': str
            },
            'description': {
                'expected': str
            },
            'ticket_duration': {
                'expected': int
            },
            'ticket_estimation': {
                'expected': int
            },
            'project': {
                'expected': dict
            },
            'project.id': {
                'expected': int
            },
            'project.display_name': {
                'expected': str
            },
            'project.url': {
                'expected': Hyperlink
            },
            'milestone': {
                'expected': dict
            },
            'milestone.id': {
                'expected': int
            },
            'milestone.display_name': {
                'expected': str
            },
            'milestone.url': {
                'expected': str
            },
            'urgency': {
                'expected': int
            },
            'urgency_badge': {
                'expected': dict
            },
            'urgency_badge.icon': {
                'expected': dict
            },
            'urgency_badge.icon.name': {
                'expected': str
            },
            'urgency_badge.icon.style': {
                'expected': str
            },
            'urgency_badge.text': {
                'expected': str
            },
            'urgency_badge.text_style': {
                'expected': str
            },
            'urgency_badge.url': {
                'expected': type(None)
            },
            'impact': {
                'expected': int
            },
            'impact_badge': {
                'expected': dict
            },
            'impact_badge.icon': {
                'expected': dict
            },
            'impact_badge.icon.name': {
                'expected': str
            },
            'impact_badge.icon.style': {
                'expected': str
            },
            'impact_badge.text': {
                'expected': str
            },
            'impact_badge.text_style': {
                'expected': str
            },
            'impact_badge.url': {
                'expected': type(None)
            },
            'priority': {
                'expected': int
            },
            'priority_badge': {
                'expected': dict
            },
            'priority_badge.icon': {
                'expected': dict
            },
            'priority_badge.icon.name': {
                'expected': str
            },
            'priority_badge.icon.style': {
                'expected': str
            },
            'priority_badge.text': {
                'expected': str
            },
            'priority_badge.text_style': {
                'expected': str
            },
            'priority_badge.url': {
                'expected': type(None)
            },
            'opened_by': {
                'expected': dict
            },
            'opened_by.id': {
                'expected': int
            },
            'opened_by.display_name': {
                'expected': str
            },
            'opened_by.first_name': {
                'expected': str
            },
            'opened_by.last_name': {
                'expected': str
            },
            'opened_by.username': {
                'expected': str
            },
            'opened_by.username': {
                'expected': str
            },
            'opened_by.is_active': {
                'expected': bool
            },
            'opened_by.url': {
                'expected': Hyperlink
            },

            'subscribed_to': {
                'expected': list
            },
            'subscribed_to.0.id': {
                'expected': int
            },
            'subscribed_to.0.display_name': {
                'expected': str
            },
            'subscribed_to.0.url': {
                'expected': str
            },

            'assigned_to': {
                'expected': list
            },
            'assigned_to.0.id': {
                'expected': int
            },
            'assigned_to.0.display_name': {
                'expected': str
            },
            'assigned_to.0.url': {
                'expected': str
            },

            'planned_start_date': {
                'expected': str
            },
            'planned_finish_date': {
                'expected': str
            },
            'real_start_date': {
                'expected': str
            },
            'real_finish_date': {
                'expected': str
            },

            'is_deleted': {
                'expected': bool
            },
            'is_solved': {
                'expected': bool
            },
            'date_solved': {
                'expected': str
            },
            'is_closed': {
                'expected': bool
            },
            'date_closed': {
                'expected': str
            },

        }


    # def test_api_field_value_ticket_type(self):
    #     """ Test for value of an API Field

    #     **note:** you must override this test with the correct value for
    #     your ticket type

    #     ticket_type field must be 'ticket'
    #     """

    #     assert self.api_data['ticket_type'] == 'ticket'



class TicketBaseAPIInheritedCases(
    APITestCases,
):

    pass


@pytest.mark.module_core
class TicketBaseAPIPyTest(
    APITestCases,
):

    pass
