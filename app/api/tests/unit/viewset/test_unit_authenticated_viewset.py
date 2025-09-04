import pytest

from rest_framework.permissions import (
    IsAuthenticated,
)

from api.tests.unit.test_unit_common_viewset import (
    CommonReadOnlyModelViewSetInheritedCases,
    ModelViewSetBaseCases,
)

from api.viewsets.common.authenticated import (
    AuthUserReadOnlyModelViewSet,
    IndexViewset,

)



@pytest.mark.permissions_authenticated_user
@pytest.mark.permissions
class AuthUserReadOnlyModelViewSetTestCases(
    CommonReadOnlyModelViewSetInheritedCases
):

    @property
    def parameterized_class_attributes(self):
        return {
            'permission_classes': {
                'type': list,
                'value': [
                    IsAuthenticated,
                ]
            },

        }


class AuthUserReadOnlyModelViewSetInheritedCases(
    AuthUserReadOnlyModelViewSetTestCases
):
    pass

class AuthenticatedUserPermissionsReadOnlyModelViewSetPyTest(
    AuthUserReadOnlyModelViewSetTestCases
):
    @pytest.fixture
    def viewset(self):
        yield AuthUserReadOnlyModelViewSet

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

    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_calls_user(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_filters_by_pk(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_filters_by_model_id(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



@pytest.mark.permissions_authenticated_user
@pytest.mark.permissions
class IndexViewsetTestCases(
    ModelViewSetBaseCases,
):

    @property
    def parameterized_class_attributes(self):
        return {
            'permission_classes': {
                'type': list,
                'value': [
                    IsAuthenticated,
                ]
            },

        }

    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_calls_user(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_filters_by_pk(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_filters_by_model_id(self):
        pytest.xfail( reason = 'base class is abstract with no model' )


class IndexViewsetInheritedCases(
    IndexViewsetTestCases,
):
    pass

class AuthenticatedUserPermissionsIndexViewsetPyTest(
    IndexViewsetTestCases,
):
    @pytest.fixture
    def viewset(self):
        yield IndexViewset

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

    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_calls_user(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_filters_by_pk(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_filters_by_model_id(self):
        pytest.xfail( reason = 'base class is abstract with no model' )
