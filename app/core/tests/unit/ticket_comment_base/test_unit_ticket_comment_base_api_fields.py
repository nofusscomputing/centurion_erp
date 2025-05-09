import pytest

from django.contrib.auth.models import ContentType, Permission, User

from rest_framework.relations import Hyperlink

from app.tests.common import DoesNotExist

from api.tests.unit.test_unit_api_fields import (
    APIFieldsInheritedCases,
)

from core.models.ticket_comment_base import (
    Entity,
    TicketBase,
    TicketCommentBase,
    TicketCommentCategory
)



class TicketCommentBaseAPITestCases(
    APIFieldsInheritedCases,
):

    base_model = TicketCommentBase


    @pytest.fixture( scope = 'class')
    def setup_model(self, request, django_db_blocker,
        model,
    ):

        with django_db_blocker.unblock():


            ticket_view_permission = Permission.objects.get(
                    codename = 'view_' + TicketBase._meta.model_name,
                    content_type = ContentType.objects.get(
                        app_label = TicketBase._meta.app_label,
                        model = TicketBase._meta.model_name,
                    )
                )

            request.cls.view_team.permissions.add( ticket_view_permission )




            category = TicketCommentCategory.objects.create(
                organization = request.cls.organization,
                name = 'comment category'
            )

            ticket_user = User.objects.create_user(username="ticket_user", password="password")

            ticket = TicketBase.objects.create(
                organization = request.cls.organization,
                title = 'ticket comment title',
                opened_by = ticket_user,
            )


            comment_user = Entity.objects.create(
                organization = request.cls.organization,
            )


            valid_data = request.cls.kwargs_create_item.copy()

            valid_data['body'] = 'the parent comment'
            valid_data['user'] = comment_user
            valid_data['ticket'] = ticket
            valid_data['comment_type'] = TicketCommentBase._meta.sub_model_type

            del valid_data['external_ref']
            del valid_data['external_system']
            del valid_data['category']
            del valid_data['parent']
            del valid_data['template']

            parent_comment = TicketCommentBase.objects.create(
                **valid_data
            )


            valid_data['body'] = 'the template comment'

            template_comment = TicketCommentBase.objects.create(
                **valid_data
            )


            request.cls.kwargs_create_item.update({
                'category': category,
                'ticket': ticket,
                'user': comment_user,
                'parent': parent_comment,
                'template': template_comment,
                'comment_type': model._meta.sub_model_type
            })



        yield



        with django_db_blocker.unblock():

            parent_comment.delete()

            template_comment.delete()

            category.delete()


            for comment in ticket.ticketcommentbase_set.all():

                comment.delete()

            ticket.delete()

            ticket_user.delete()





    @pytest.fixture( scope = 'class')
    def post_model(self, request, model ):

        request.cls.url_view_kwargs.update({
            'ticket_id': request.cls.item.ticket.id
        })

        if (
            model != self.base_model
            or self.item.parent
        ):

            request.cls.url_view_kwargs.update({
                'ticket_comment_model': model._meta.sub_model_type
            })

        if self.item.parent:

            request.cls.url_ns_name = '_api_v2_ticket_comment_base_sub_thread'

            request.cls.url_view_kwargs.update({
                'parent_id': self.item.parent.id
            })







    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self, request, django_db_blocker,
        setup_pre,
        setup_model,
        create_model,
        post_model,
        setup_post,
    ):

        pass



    @property
    def parameterized_test_data(self):
        
        return {

        'parent': {
            'expected': dict
        },
        'parent.id': {
            'expected': int
        },
        'parent.display_name': {
            'expected': str
        },
        'parent.url': {
            'expected': str
        },


        'ticket': {
            'expected': dict
        },
        'ticket.id': {
            'expected': int
        },
        'ticket.display_name': {
            'expected': str
        },
        'ticket.url': {
            'expected': str
        },

        'external_ref': {
            'expected': int
        },
        'external_system': {
            'expected': int
        },
        'comment_type': {
            'expected': str
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

        'body': {
            'expected': str
        },
        'private': {
            'expected': bool
        },
        'duration': {
            'expected': int
        },
        'estimation': {
            'expected': int
        },
        'template': {
            'expected': dict
        },
        'template.id': {
            'expected': int
        },
        'template.display_name': {
            'expected': str
        },
        'template.url': {
            'expected': str
        },

        'is_template': {
            'expected': bool
        },
        'source': {
            'expected': int
        },
        'user': {
            'expected': dict
        },
        'user.id': {
            'expected': int
        },
        'user.display_name': {
            'expected': str
        },
        'user.url': {
            'expected': Hyperlink
        },

        'is_closed': {
            'expected': bool
        },
        'date_closed': {
            'expected': str
        },

        '_urls.threads': {
            'expected': str
        },
        # Below fields dont exist.

        'display_name': {
            'expected': DoesNotExist
        },
        'model_notes': {
            'expected': DoesNotExist
        },
        '_urls.notes': {
            'expected': DoesNotExist
        },
    }



    kwargs_create_item: dict = {
        'parent': '',
        'ticket': '',
        'external_ref': 123,
        'external_system': TicketBase.Ticket_ExternalSystem.CUSTOM_1,
        'comment_type': '',
        'category': '',
        'body': 'the ticket comment',
        'private': False,
        'duration': 1,
        'estimation': 2,
        'template': '',
        'is_template': True,
        'source': TicketBase.TicketSource.HELPDESK,
        'user': '',
        'is_closed': True,
        'date_closed': '2025-05-09T19:32Z',
    }



    url_ns_name = '_api_v2_ticket_comment_base'
    """Url namespace (optional, if not required) and url name"""



class TicketCommentBaseAPIInheritedCases(
    TicketCommentBaseAPITestCases,
):

    kwargs_create_item: dict = None

    model = None

    url_ns_name = '_api_v2_ticket_comment_base_sub'



class TicketCommentBaseAPIPyTest(
    TicketCommentBaseAPITestCases,
):

    pass
