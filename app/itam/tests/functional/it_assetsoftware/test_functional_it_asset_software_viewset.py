import pytest

from rest_framework.permissions import OperandHolder

from accounting.viewsets.asset import (
    NoDocsViewSet,
    ViewSet,
)

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases



@pytest.mark.model_itasset
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'Model is not a centurion model' )
    def test_function_get_queryset_filtered_results_action_list_user_tenancies_only(self,
        viewset_mock_request, organization_one, organization_two, model,
        api_request_permissions,
    ):
        """Test class function

        Ensure that when function `get_queryset` returns values that are filtered
        to the users tenancies only.
        """

        viewset = viewset_mock_request

        viewset.action = 'list'

        viewset.allowed_methods = [ 'GET' ]

        if not viewset.model:
            pytest.xfail( reason = 'no model exists, assuming viewset is a base/mixin viewset.' )

        only_user_results_returned = True

        for permission_class in viewset.permission_classes:

            if isinstance(permission_class, OperandHolder):
                permission_class = permission_class.op1_class


            permission_class().has_permission(request = viewset.request, view = viewset)

        queryset = viewset.get_queryset()

        assert len(model.objects.all()) >= 2, 'multiple objects must exist for test to work'
        assert len( queryset ) > 0, 'Empty queryset returned. Test not possible'
        if model._meta.model_name != 'tenant':
            assert len(model.objects.filter( organization = organization_one)) > 0, 'objects in user org required for test to work.'
            assert len(model.objects.filter( organization = organization_two)) > 0, 'objects in different org required for test to work.'


        for result in queryset:

            
            if result.get_tenant() not in [
                api_request_permissions['tenancy']['global'],    # Global tenancy
                organization_one
            ]:
                only_user_results_returned = False

        assert only_user_results_returned



class ITAssetViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetViewsetPyTest(
    ViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet
