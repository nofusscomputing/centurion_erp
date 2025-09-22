import pytest
import random

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)

from core.models.ticket_comment_base import (
    TicketBase,
    TicketCommentBase,
)


@pytest.mark.model_ticketcommentbase
class TicketCommentBaseAPIFieldsTestCases(
    APIFieldsInheritedCases,
):

    base_model = TicketCommentBase



    @pytest.fixture( scope = 'class')
    def create_model(self, request, django_db_blocker,
        model, model_kwargs
    ):

        with django_db_blocker.unblock():


            kwargs = model_kwargs.copy()

            kwargs['body'] = 'the template comment'

            del kwargs['external_ref']
            del kwargs['external_system']
            del kwargs['category']

            kwargs['comment_type'] = model._meta.sub_model_type
            kwargs['is_template'] = True

            template_comment = model.objects.create(
                **kwargs
            )


            kwargs = model_kwargs.copy()
            kwargs['template'] = template_comment

            kwargs['ticket'].is_closed = False
            kwargs['ticket'].date_closed = None
            kwargs['ticket'].is_solved = False
            kwargs['ticket'].date_solved = None
            kwargs['ticket'].status = TicketBase.TicketStatus.NEW
            kwargs['ticket'].save()

            kwargs['external_ref'] = random.randint(333, 33333)

            item = model.objects.create(
                **kwargs
            )

            request.cls.item = item


            kwargs = model_kwargs.copy()
            kwargs['body'] = 'the child comment'
            kwargs['comment_type'] = model._meta.sub_model_type
            kwargs['parent'] = request.cls.item

            del kwargs['external_ref']
            del kwargs['external_system']
            del kwargs['category']

            kwargs['ticket'].is_closed = False
            kwargs['ticket'].date_closed = None
            kwargs['ticket'].is_solved = False
            kwargs['ticket'].date_solved = None
            kwargs['ticket'].status = TicketBase.TicketStatus.NEW
            kwargs['ticket'].save()


            item_two = model.objects.create(
                **kwargs
            )

            request.cls.item_two = item_two

            yield item

            item_two.delete()

            item.delete()

            template_comment.delete()



    @property
    def parameterized_api_fields(self):

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
                'expected': str
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
                'expected': models.NOT_PROVIDED
            },
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            '_urls.notes': {
                'expected': models.NOT_PROVIDED
            },
        }



class TicketCommentBaseAPIFieldsInheritedCases(
    TicketCommentBaseAPIFieldsTestCases,
):

    pass



@pytest.mark.module_core
class TicketCommentBaseAPIFieldsPyTest(
    TicketCommentBaseAPIFieldsTestCases,
):

    pass
