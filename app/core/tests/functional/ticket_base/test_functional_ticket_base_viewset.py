
import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.viewsets.ticket import (
    ViewSet,
)



@pytest.mark.model_ticketbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @pytest.mark.skip( reason = 'To be written.' )
    def test_permission_triage_task_comment_create(self):
        """Ticket Permission Check
        
        Only a user with permission `triage` on the ticket being edited
        can `create` a ticket task comment
        """
        pass


    @pytest.mark.skip( reason = 'To be written.' )
    def test_permission_triage_task_comment_edit(self):
        """Ticket Permission Check
        
        Only a user with permission `triage` on the ticket being edited
        can `create` a ticket task comment
        """
        pass


    @pytest.mark.skip( reason = 'To be written.' )
    def test_permission_triage_task_comment_delete(self):
        """Ticket Permission Check
        
        Only a user with permission `triage` on the ticket being edited
        can `create` a ticket task comment
        """
        pass


class TicketBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
