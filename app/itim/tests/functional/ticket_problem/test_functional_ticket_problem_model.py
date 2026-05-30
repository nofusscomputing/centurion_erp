import pytest

from django.db import models

from core.tests.functional.ticket_base.test_functional_ticket_base_model import (
    TicketBaseModelInheritedTestCases
)



@pytest.mark.model_problemticket
class ProblemTicketModelTestCases(
    TicketBaseModelInheritedTestCases
):

    @property
    def parameterized_model_fields(self):

        return {
            'business_impact': {
                'field': 'business_impact',
                'type': models.TextField,
            },
            'cause_analysis': {
                'field': 'cause_analysis',
                'type': models.TextField,
            },
            'observations': {
                'field': 'observations',
                'type': models.TextField,
            },
            'workaround': {
                'field': 'workaround',
                'type': models.TextField,
            },
        }



class ProblemTicketModelInheritedTestCases(
    ProblemTicketModelTestCases
):

    pass


@pytest.mark.module_itim
class ProblemTicketModelPyTest(
    ProblemTicketModelTestCases
):

    pass
