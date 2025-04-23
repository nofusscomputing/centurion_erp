import pytest

from rest_framework.relations import Hyperlink

from access.models.entity import Entity

from api.tests.unit.test_unit_api_fields import (
    APIFieldsInheritedCases,
    DoesNotExist,
)

from core.models.ticket.ticket_category import TicketCategory

from project_management.models.project_milestone import Project, ProjectMilestone



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
            })


            if request.cls.model._meta.model_name != 'ticketbase':

                request.cls.url_view_kwargs.update({
                    'ticket_model': str(request.cls.model._meta.verbose_name).lower().replace(' ', '_'),
                })

        yield

        with django_db_blocker.unblock():

            request.cls.entity_user.delete()

            parent_ticket.delete()

            project_milestone.delete()

            project.delete()

            request.cls.kwargs_create_item['category'].delete()

            if 'ticket_model' in request.cls.url_view_kwargs:

                del request.cls.url_view_kwargs['ticket_model']



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


    parametrized_test_data = {
        'model_notes': DoesNotExist,
        '_urls.notes': DoesNotExist,
        'external_system': int,
        'external_ref': int,
        'parent_ticket': dict,
        'parent_ticket.id': int,
        'parent_ticket.display_name': str,
        'parent_ticket.url': str,
        'ticket_type': str,
        'status': int,
        'status_badge': dict,
        'status_badge.icon': dict,
        'status_badge.icon.name': str,
        'status_badge.icon.style': str,
        'status_badge.text': str,
        'status_badge.text_style': str,
        'status_badge.url': type(None),
        'category': dict,
        'category.id': int,
        'category.display_name': str,
        'category.url': Hyperlink,
        'title': str,
        'description': str,
        'ticket_duration': int,
        'ticket_estimation': int,
        'project': dict,
        'project.id': int,
        'project.display_name': str,
        'project.url': Hyperlink,
        'milestone': dict,
        'milestone.id': int,
        'milestone.display_name': str,
        'milestone.url': str,
        'urgency': int,
        'urgency_badge': dict,
        'urgency_badge.icon': dict,
        'urgency_badge.icon.name': str,
        'urgency_badge.icon.style': str,
        'urgency_badge.text': str,
        'urgency_badge.text_style': str,
        'urgency_badge.url': type(None),
        'impact': int,
        'impact_badge': dict,
        'impact_badge.icon': dict,
        'impact_badge.icon.name': str,
        'impact_badge.icon.style': str,
        'impact_badge.text': str,
        'impact_badge.text_style': str,
        'impact_badge.url': type(None),
        'priority': int,
        'priority_badge': dict,
        'priority_badge.icon': dict,
        'priority_badge.icon.name': str,
        'priority_badge.icon.style': str,
        'priority_badge.text': str,
        'priority_badge.text_style': str,
        'priority_badge.url': type(None),
        'opened_by': dict,
        'opened_by.id': int,
        'opened_by.display_name': str,
        'opened_by.first_name': str,
        'opened_by.last_name': str,
        'opened_by.username': str,
        'opened_by.username': str,
        'opened_by.is_active': bool,
        'opened_by.url': Hyperlink,

        'subscribed_to': list,
        'subscribed_to.0.id': int,
        'subscribed_to.0.display_name': str,
        'subscribed_to.0.url': str,

        'assigned_to': list,
        'assigned_to.0.id': int,
        'assigned_to.0.display_name': str,
        'assigned_to.0.url': str,

        'planned_start_date': str,
        'planned_finish_date': str,
        'real_start_date': str,
        'real_finish_date': str,

        'is_deleted': bool,
        'is_solved': bool,
        'date_solved': str,
        'is_closed': bool,
        'date_closed': str,

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
        'is_closed': True,
    }

    url_ns_name = '_api_v2_ticket'
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

    url_ns_name = '_api_v2_ticket_sub'



class TicketBaseAPIPyTest(
    APITestCases,
):

    pass
