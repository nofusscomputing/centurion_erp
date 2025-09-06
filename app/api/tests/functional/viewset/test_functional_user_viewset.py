import pytest

from api.tests.functional.test_functional_common_viewset import (
    CommonModelCreateViewSetInheritedCases,
    CommonModelListRetrieveDeleteViewSetInheritedCases,
    CommonModelRetrieveUpdateViewSetInheritedCases,
)
from api.viewsets.common.user import (
    ModelCreateViewSet,
    ModelListRetrieveDeleteViewSet,
    ModelRetrieveUpdateViewSet,
)



@pytest.mark.permissions_user
@pytest.mark.permissions
class ModelCreateViewSetTestCases(
    CommonModelCreateViewSetInheritedCases,
):

    # parmeterize to view action
    def test_function_get_queryset_filtered_results_action_list(self,
        viewset_mock_request, organization_one, model
    ):
        """Test class function

        Ensure that when function `get_queryset` returns values that are filtered
        """

        viewset = viewset_mock_request

        viewset.action = 'list'

        if not viewset.model:
            pytest.xfail( reason = 'no model exists, assuming viewset is a base/mixin viewset.' )

        only_user_results_returned = True

        queryset = viewset.get_queryset()

        assert len(model.objects.all()) >= 2, 'multiple objects must exist for test to work'
        assert len( queryset ) > 0, 'Empty queryset returned. Test not possible'

        for result in queryset:

            if result.user != self.user:
                only_user_results_returned = False

        assert only_user_results_returned


class ModelCreateViewSetInheritedCases(
    ModelCreateViewSetTestCases,
):
    pass

class UserPermissionsModelCreateViewSetPyTest(
    ModelCreateViewSetTestCases,
):
    @pytest.fixture
    def viewset(self):
        yield ModelCreateViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.permissions_user
@pytest.mark.permissions
class ModelListRetrieveDeleteViewSetTestCases(
    CommonModelListRetrieveDeleteViewSetInheritedCases,
):

    # parmeterize to view action
    def test_function_get_queryset_filtered_results_action_list(self,
        viewset_mock_request, organization_one, model
    ):
        """Test class function

        Ensure that when function `get_queryset` returns values that are filtered
        """

        viewset = viewset_mock_request

        viewset.action = 'list'

        if not viewset.model:
            pytest.xfail( reason = 'no model exists, assuming viewset is a base/mixin viewset.' )

        only_user_results_returned = True

        queryset = viewset.get_queryset()

        assert len(model.objects.all()) >= 2, 'multiple objects must exist for test to work'
        assert len( queryset ) > 0, 'Empty queryset returned. Test not possible'

        for result in queryset:

            if result.user != self.user:
                only_user_results_returned = False

        assert only_user_results_returned


class ModelListRetrieveDeleteViewSetInheritedCases(
    ModelListRetrieveDeleteViewSetTestCases,
):
    pass

class UserPermissionsModelListRetrieveDeleteViewSetPyTest(
    ModelListRetrieveDeleteViewSetTestCases,
):
    @pytest.fixture
    def viewset(self):
        yield ModelListRetrieveDeleteViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.permissions_user
@pytest.mark.permissions
class ModelRetrieveUpdateViewSetTestCases(
    CommonModelRetrieveUpdateViewSetInheritedCases,
):

    # parmeterize to view action
    def test_function_get_queryset_filtered_results_action_list(self,
        viewset_mock_request, organization_one, model
    ):
        """Test class function

        Ensure that when function `get_queryset` returns values that are filtered
        """

        viewset = viewset_mock_request

        viewset.action = 'list'

        if not viewset.model:
            pytest.xfail( reason = 'no model exists, assuming viewset is a base/mixin viewset.' )

        only_user_results_returned = True

        queryset = viewset.get_queryset()

        assert len(model.objects.all()) >= 2, 'multiple objects must exist for test to work'
        assert len( queryset ) > 0, 'Empty queryset returned. Test not possible'

        for result in queryset:

            if result.user != self.user:
                only_user_results_returned = False

        assert only_user_results_returned


class ModelRetrieveUpdateViewSetInheritedCases(
    ModelRetrieveUpdateViewSetTestCases,
):
    pass

class UserPermissionsModelRetrieveUpdateViewSetPyTest(
    ModelRetrieveUpdateViewSetTestCases,
):
    @pytest.fixture
    def viewset(self):
        yield ModelRetrieveUpdateViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )
