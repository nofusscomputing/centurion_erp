import pytest

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from project_management.viewsets.project import (
    Project,
    ViewSet,
)


class MockRequest:

    data = {}


@pytest.mark.model_project
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_model_documentation': {
                'type': type(None),
            },
            'back_url': {
                'type': type(None),
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'filterset_fields': {
                'value': [
                    'organization',
                    'external_system',
                    'parent',
                    'priority',
                    'project_type',
                    'state'
                ]
            },
            'model': {
                'value': Project
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'name',
                    'description'
                ]
            },
            'view_description': {
                'value': 'Physical Devices'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires request object' )
    def test_view_func_get_serializer_class_create(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct create
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'create'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_create_request_data(self,
        viewset, model, model_serializer, mocker
    ):
        """ Function Test

        Function `get_serializer_class` must return the correct create
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'create'

        viewset.request = MockRequest()

        mocker.patch.object(view_set, 'get_queryset', return_value = [])

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires request object' )
    def test_view_func_get_serializer_class_partial_update(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct partial_update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'partial_update'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_partial_update_request_data(self,
        viewset, model, model_serializer, mocker
    ):
        """ Function Test

        Function `get_serializer_class` must return the correct partial_update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'partial_update'

        viewset.request = MockRequest()

        mocker.patch.object(view_set, 'get_queryset', return_value = [])

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires request object' )
    def test_view_func_get_serializer_class_update(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'update'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_update_request_data(self,
        viewset, model, model_serializer, mocker
    ):
        """ Function Test

        Function `get_serializer_class` must return the correct update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'update'

        viewset.request = MockRequest()

        mocker.patch.object(view_set, 'get_queryset', return_value = [])

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires request object' )
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'


        assert view_set.get_serializer_class() == model_serializer['view']



    def test_view_func_get_serializer_class_view_request_data(self,
        viewset, model, model_serializer, mocker
    ):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'

        viewset.request = MockRequest()

        mocker.patch.object(view_set, 'get_queryset', return_value = [])

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['view']



class ProjectViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectViewsetPyTest(
    ViewsetTestCases,
):

    pass
