import pytest

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_ticketcommentcategory
class TicketCommentCategoryAPITestCases(
    APIFieldsInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'name': {
                'expected': str
            },
            # 'change': {
            #     'expected': bool
            # },
            # 'incident': {
            #     'expected': bool
            # },
            # 'problem': {
            #     'expected': bool
            # },
            # 'project_task': {
            #     'expected': bool
            # },
            # 'request': {
            #     'expected': bool
            # },
            'parent': {
                'expected': type(None)
            },
            # 'runbook': {
            #     'expected': type(None)
            # },
            'modified': {
                'expected': str
            }
        }



class TicketCommentCategoryAPIInheritedCases(
    TicketCommentCategoryAPITestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentCategoryAPIPyTest(
    TicketCommentCategoryAPITestCases,
):

    pass
