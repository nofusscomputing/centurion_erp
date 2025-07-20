import django
import pytest

from rest_framework.relations import Hyperlink

from access.models.entity import Entity

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
    DoesNotExist,
)

from core.models.ticket.ticket_category import TicketCategory

from project_management.models.project_milestone import Project, ProjectMilestone



@pytest.mark.model_ticketbase
class APITestCases(
    APIFieldsInheritedCases,
):


    @pytest.fixture( scope = 'class')
    def setup_model(self, request, django_db_blocker,
        model,
    ):

        with django_db_blocker.unblock():

            request.cls.entity_user = Entity.objects.create(
                organization = request.cls.organization,
                model_notes = 'asdas'
            )

            project = Project.objects.create(
                organization = request.cls.organization,
                name = 'project'
            )

            parent_ticket = request.cls.model.objects.create(
                organization = request.cls.organization,
                title = 'parent ticket',
                description = 'bla bla',
                opened_by = request.cls.view_user,
            )

            project_milestone = ProjectMilestone.objects.create(
                organization = request.cls.organization,
                name = 'project milestone one',
                project = project
            )

            request.cls.kwargs_create_item.update({
                'category': TicketCategory.objects.create(
                organization = request.cls.organization,
                    name = 'a category'
                ),
                'opened_by': request.cls.view_user,
                'project': project,
                'milestone': project_milestone,
                'parent_ticket': parent_ticket,
                'external_system': int(request.cls.model.Ticket_ExternalSystem.CUSTOM_1),
                'impact': int(request.cls.model.TicketImpact.MEDIUM),
                'priority': int(request.cls.model.TicketPriority.HIGH),
                'status': request.cls.model.TicketStatus.CLOSED,
            })


            if request.cls.model._meta.sub_model_type != 'ticket':

                request.cls.url_view_kwargs.update({
                    'ticket_type': str(request.cls.model._meta.sub_model_type),
                })

        yield

        with django_db_blocker.unblock():

            request.cls.entity_user.delete()

            parent_ticket.delete()

            try:
                project_milestone.delete()
            except django.db.models.deletion.ProtectedError:
                pass

            try:
                project.delete()
            except django.db.models.deletion.ProtectedError:
                pass

            try:
                request.cls.kwargs_create_item['category'].delete()
            except django.db.models.deletion.ProtectedError:
                pass

            if 'ticket_type' in request.cls.url_view_kwargs:

                del request.cls.url_view_kwargs['ticket_type']



    @pytest.fixture( scope = 'class')
    def post_model_create(self, request, django_db_blocker):

        with django_db_blocker.unblock():

            request.cls.item.assigned_to.add(request.cls.entity_user.id)
            request.cls.item.subscribed_to.add(request.cls.entity_user.id)



    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_pre,
        setup_model,
        create_model,
        post_model_create,
        setup_post,
    ):

        pass


    parameterized_test_data = {
        'model_notes': {
            'expected': DoesNotExist
        },
        '_urls.notes': {
            'expected': DoesNotExist
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

    kwargs_create_item: dict = {
        'external_ref': 1,
        'title': 'ticket title',
        'description': 'the ticket description',
        'planned_start_date': '2025-04-16T00:00:01',
        'planned_finish_date': '2025-04-16T00:00:02',
        'real_start_date': '2025-04-16T00:00:03',
        'real_finish_date': '2025-04-16T00:00:04',
        'is_solved': True,
        'date_solved': '2025-05-12T02:30:01',
        'is_closed': True,
        'date_closed': '2025-05-12T02:30:02',
    }

    url_ns_name = '_api_ticketbase'
    """Url namespace (optional, if not required) and url name"""


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

    kwargs_create_item: dict = None

    model = None

    url_ns_name = '_api_ticketbase_sub'


@pytest.mark.module_core
class TicketBaseAPIPyTest(
    APITestCases,
):

    pass
