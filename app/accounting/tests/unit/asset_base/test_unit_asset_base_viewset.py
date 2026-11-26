import pytest

from accounting.viewsets.asset import (
    NoDocsViewSet,
    AssetBase,
    ViewSet,
)

from api.tests.unit.viewset.test_unit_tenancy_viewset import SubModelViewSetInheritedCases



@pytest.mark.model_assetbase
class AssetBaseViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            # '_log': {
            #     'type': logging.Logger,
            #     'value': None
            # },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'base_model': {
                'value': AssetBase
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'filterset_fields': {
                'value': [
                    'asset_number',
                    'serial_number',
                    'organization',
                ]
            },
            'model': {
                'value': AssetBase
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'model_kwarg': {
                'value': 'model_name'
            },
            'model_suffix': {
                'type': type(None)
            },
            'queryset': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'search_fields': {
                'value': [
                    'asset_number',
                    'serial_number',
                ]
            },
            'view_description': {
                'value': 'All Assets'
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }



class AssetBaseViewsetInheritedCases(
    AssetBaseViewsetTestCases,
):

    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires kwarg `model_name`' )
    def test_view_func_get_serializer_class_create(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct create
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'create'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_create_kwargs(self, viewset, model, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct create
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'create'

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires kwarg `model_name`' )
    def test_view_func_get_serializer_class_partial_update(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct partial_update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'partial_update'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_partial_update_kwargs(self, viewset, model, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct partial_update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'partial_update'

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires kwarg `model_name`' )
    def test_view_func_get_serializer_class_update(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'update'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_update_kwargs(self, viewset, model, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'update'

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires kwarg `model_name`' )
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'


        assert view_set.get_serializer_class() == model_serializer['view']



    def test_view_func_get_serializer_class_view_kwargs(self, viewset, model, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['view']




@pytest.mark.module_accounting
class AssetBaseViewsetPyTest(
    AssetBaseViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet
