import pytest

from access.permissions.user import UserPermissions

from api.tests.unit.test_unit_common_viewset import (
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

    @property
    def parameterized_class_attributes(self):
        return {
            'permission_classes': {
                'type': list,
                'value': [
                    UserPermissions,
                ]
            },

        }

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
    def test_view_func_get_serializer_class_create(self):
        assert False

    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_view(self):
        assert False



@pytest.mark.permissions_user
@pytest.mark.permissions
class ModelListRetrieveDeleteViewSetTestCases(
    CommonModelListRetrieveDeleteViewSetInheritedCases,
):

    @property
    def parameterized_class_attributes(self):
        return {
            'permission_classes': {
                'type': list,
                'value': [
                    UserPermissions,
                ]
            },

        }

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
    def test_view_func_get_serializer_class_view(self):
        assert False



@pytest.mark.permissions_user
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
                    UserPermissions,
                ]
            },

        }

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
        assert False


    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_update(self, viewset, model_serializer):
        assert False


    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        assert False
