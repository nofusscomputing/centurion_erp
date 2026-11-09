import pytest

from django.db import models

from itam.tests.functional.it_asset_related_viewset.test_functional_it_asset_related_viewset import (
    ITAssetRelatedViewsetInheritedCases
)
from itam.viewsets.it_asset_connection import (
    ViewSet
)

from itam.viewsets.it_asset_related import ViewSet as RelatedViewSet



@pytest.mark.model_itassetrelationships
class ViewsetTestCases(
    ITAssetRelatedViewsetInheritedCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



    def test_queryset_itasset(self, viewset_mock_request, mocker,
        model_itassetrelationships, kwargs_itassetrelationships,
    ):
        """Test ViewSet QuerySet

        When the parent model is itasset, the queryset must be filtered
        so that the connections are those for the itasset.
        """

        kwargs = kwargs_itassetrelationships(parent_model = True)

        parent_model = kwargs['parent']

        asset_model = parent_model.device_model

        model_itassetrelationships.objects.create(
            **kwargs
        )

        viewset = viewset_mock_request

        viewset.action = 'list'

        viewset.allowed_methods = [ 'GET' ]

        viewset.kwargs = {
            'model_name': parent_model._meta.model_name,
            'model_id': parent_model.pk,
            'related_model_name': 'connections'
        }

        viewset._queryset = None

        filter = mocker.spy(models.QuerySet, 'filter')

        filter.reset_mock()

        viewset.get_queryset()


        assert not any(
            call.kwargs.get("parent", '-does-not-exist-') == None
                and call.args[0].model is model_itassetrelationships
                    for call in filter.call_args_list
        ), 'Test cant continue if the parent has been filtered to None.'



    def test_queryset_itassetmodel(self, viewset_mock_request, mocker,
        model_itassetrelationships, kwargs_itassetrelationships,
    ):
        """Test ViewSet QuerySet
        
        When the parent model is itassetmodel, the queryset must be filtered
        to those that are for the itassetmodel.
        """

        kwargs = kwargs_itassetrelationships(parent_model = False)

        asset_model = kwargs['parent_asset_model']

        model_itassetrelationships.objects.create(
            **kwargs
        )

        viewset = viewset_mock_request

        viewset.action = 'list'

        viewset.allowed_methods = [ 'GET' ]

        viewset.kwargs = {
            'model_name': asset_model._meta.model_name,
            'model_id': asset_model.pk,
            'related_model_name': 'connections'
        }

        viewset._queryset = None

        filter = mocker.spy(models.QuerySet, 'filter')

        filter.reset_mock()

        viewset.get_queryset()

        assert any(
            call.kwargs.get("parent", '-does-not-exist-') == None
                and call.args[0].model is model_itassetrelationships
                    for call in filter.call_args_list
        )



class ITAssetRelationshipsViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetRelationshipsViewsetPyTest(
    ViewsetTestCases,
):
    pass
