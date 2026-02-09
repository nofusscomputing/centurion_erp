import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_ticketcommentcategory
class TicketCommentCategoryModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class TicketCommentCategoryModelInheritedCases(
    TicketCommentCategoryModelTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentCategoryModelPyTest(
    TicketCommentCategoryModelTestCases,
):
    pass
