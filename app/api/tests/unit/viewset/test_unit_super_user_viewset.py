import pytest

from access.permissions.super_user import SuperUserPermissions

from api.tests.unit.test_unit_common_viewset import (
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

    @property
    def parameterized_class_attributes(self):
        return {
            'permission_classes': {
                'type': list,
                'value': [
                    SuperUserPermissions,
                ]
            },

        }

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

    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
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

    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_queryset_cache_result(self):
        assert False

    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_queryset_cache_result_used(self):
        assert False

    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_function_get_queryset_manager_calls_user(self):
        assert False

    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_function_get_queryset_manager_filters_by_pk(self):
        assert False

    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_function_get_queryset_manager_filters_by_model_id(self):
        assert False


    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_partial_update(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct partial_update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'partial_update'


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_update(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'update'


        assert view_set.get_serializer_class() == model_serializer['model']


    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'


        assert view_set.get_serializer_class() == model_serializer['view']
