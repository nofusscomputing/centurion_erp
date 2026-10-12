import django
import pytest

from rest_framework.reverse import reverse

from api.tests.functional.viewset.test_functional_tenancy_viewset import SubModelViewSetInheritedCases

from accounting.viewsets.asset import (
    NoDocsViewSet,
    ViewSet,
)

from api.tests.abstract.api_serializer_viewset import SerializersTestCases



@pytest.mark.model_assetbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



    @pytest.mark.xfail( reason = 'Namespace for URL requires app_label.' )
    def test_function_get_meta_urls_self_url(self,
        viewset_mock_request, model, settings
    ):
        """Test function `get_meta_urls`

        Ensure that the `self` key is the correct value
        """


        urls = viewset_mock_request.get_meta_urls()

        assert 'self' in urls, 'self key must exist, test cant continue.'

        assert urls['self'] == reverse(
            viewname = f'v2:{viewset_mock_request.basename}-list',
            kwargs = viewset_mock_request.kwargs
        )



    def test_function_get_meta_urls_self_url_requires_app_label(self,
        viewset_mock_request, model, settings
    ):
        """Test function `get_meta_urls`

        Ensure that the `self` key is the correct value
        """


        urls = viewset_mock_request.get_meta_urls()

        assert 'self' in urls, 'self key must exist, test cant continue.'

        assert urls['self'] == reverse(
            viewname = f'v2:accounting:{viewset_mock_request.basename}-list',
            kwargs = viewset_mock_request.kwargs
        )



class AssetBaseViewSetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_accounting
class AssetBaseViewsetPyTest(
    ViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet

