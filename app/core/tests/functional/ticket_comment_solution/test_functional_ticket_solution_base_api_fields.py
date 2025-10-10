import pytest
import random

from django.db import models

from core.models.ticket_base import TicketBase
from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_api_fields import (
    TicketCommentBaseAPIFieldsInheritedCases
)



@pytest.mark.model_ticketcommentsolution
class TicketCommentSolutionAPITestCases(
    TicketCommentBaseAPIFieldsInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {

            'parent': {
                'expected': type(None)
            },
            'parent.id': {
                'expected': models.NOT_PROVIDED
            },
            'parent.display_name': {
                'expected': models.NOT_PROVIDED
            },
            'parent.url': {
                'expected': models.NOT_PROVIDED
            },

            '_urls.threads': {
                'expected': models.NOT_PROVIDED
            },
        }


    @pytest.fixture( scope = 'class')
    def create_model(self, request, django_db_blocker,
        model, model_kwargs
    ):

        with django_db_blocker.unblock():


            kwargs = model_kwargs()

            kwargs['body'] = 'the template comment'

            del kwargs['external_ref']
            del kwargs['external_system']
            del kwargs['category']

            kwargs['comment_type'] = model._meta.sub_model_type
            kwargs['is_template'] = True

            template_comment = model.objects.create(
                **kwargs
            )


            kwargs = model_kwargs()
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


            kwargs = model_kwargs()
            kwargs['body'] = 'the child comment'
            kwargs['comment_type'] = model._meta.sub_model_type
            # kwargs['parent'] = request.cls.item

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



class TicketCommentSolutionAPIInheritedCases(
    TicketCommentSolutionAPITestCases,
):

    pass



@pytest.mark.module_core
class TicketCommentSolutionAPIPyTest(
    TicketCommentSolutionAPITestCases,
):

    pass
