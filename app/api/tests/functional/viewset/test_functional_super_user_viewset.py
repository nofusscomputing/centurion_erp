import pytest

from api.tests.functional.test_functional_common_viewset import (
    CommonModelRetrieveUpdateViewSetInheritedCases,
)
from api.viewsets.common.super_user import (
    ModelRetrieveUpdateViewSet,
)



@pytest.mark.permissions_super_user
@pytest.mark.permissions
class ModelRetrieveUpdateViewSetTestCases(
    CommonModelRetrieveUpdateViewSetInheritedCases,
):

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'No filtering conducted when super user is used. test is n/a.' )

    def test_function_get_meta_urls_self_url(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_no_sub_models_key(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_sub_models_keys(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_sub_models_values(self,):
        pytest.xfail( reason = 'Base class does not require test' )



class ModelRetrieveUpdateViewSetInheritedCases(
    ModelRetrieveUpdateViewSetTestCases,
):
    pass


class SuperUserPermissionsModelRetrieveUpdateViewSetPyTest(
    ModelRetrieveUpdateViewSetTestCases,
):
    @pytest.fixture
    def viewset(self):
        yield ModelRetrieveUpdateViewSet
