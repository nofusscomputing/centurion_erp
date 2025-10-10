import pytest

# from django.db import models

# from rest_framework.relations import Hyperlink

# from api.tests.functional.test_functional_api_fields import (
#     APIFieldsInheritedCases,
# )
from core.tests.functional.model_tickets.test_functional_model_tickets_api_fields import (
    ModelTicketAPIInheritedCases
)


@pytest.mark.model_modelticket
class ModelTicketMetaAPITestCases(
    ModelTicketAPIInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'model': {
                # 'expected': models.NOT_PROVIDED,
                'type': int,
            },
            # '_urls.notes': {
            #     'expected': models.NOT_PROVIDED,
            #     'type': models.NOT_PROVIDED,
            # },
            # 'model_notes': {
            #     'expected': models.NOT_PROVIDED,
            #     'type': models.NOT_PROVIDED,
            # },
            # 'content_type': {
            #     'expected': dict
            # },
            # 'content_type.id': {
            #     'expected': int
            # },
            # 'content_type.display_name': {
            #     'expected': str
            # },
            # 'content_type.url': {
            #     'expected': Hyperlink
            # },
            # 'ticket': {
            #     'expected': dict
            # },
            # 'ticket.id': {
            #     'expected': int
            # },
            # 'ticket.display_name': {
            #     'expected': str
            # },
            # 'ticket.url': {
            #     'expected': str
            # },
            # 'modified': {
            #     'expected': str
            # }
        }



class ModelTicketMetaAPIInheritedCases(
    ModelTicketMetaAPITestCases,
):
    pass



# @pytest.mark.module_core
# class ModelTicketMetaAPIPyTest(
#     ModelTicketMetaAPITestCases,
# ):

#     pass
