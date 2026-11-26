import django
import pytest

from pytest_simplified import NOT_USED

from access.tests.unit.mixin_tenancy.test_unit_tenancy_permission_mixin import (
    TenancyMixinInheritedCases
)

from api.tests.unit.test_unit_common_viewset import (
    CommonModelViewSetInheritedCases,
    CommonModelCreateViewSetInheritedCases,
    CommonModelListRetrieveDeleteViewSetInheritedCases,
    CommonModelRetrieveUpdateViewSetInheritedCases,
    CommonSubModelViewSetTestCases,
    CommonSubModelViewSetInheritedCases,
    CommonReadOnlyModelViewSetInheritedCases,
    CommonReadOnlyListModelViewSetInheritedCases,

)
from api.viewsets.common.tenancy import (
    ModelViewSet,
    ModelCreateViewSet,
    ModelListRetrieveDeleteViewSet,
    ModelRetrieveUpdateViewSet,
    SubModelViewSet,
    ReadOnlyModelViewSet,
    ReadOnlyListModelViewSet,
)



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ModelViewSetTestCases(
    TenancyMixinInheritedCases,
    CommonModelViewSetInheritedCases,
):

    pass

class ModelViewSetInheritedCases(
    ModelViewSetTestCases,
):

    pass

class TenancyPermissionsModelViewSetPyTest(
    ModelViewSetTestCases,
):
    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelViewSet

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
    def test_view_func_get_serializer_class_create(self, viewset, model_serializer):
        assert False


    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_create(self):
        assert False


    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_partial_update(self):
        assert False


    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_update(self):
        assert False


    @pytest.mark.xfail( reason = 'base class is abstract with no model' )
    def test_view_func_get_serializer_class_view(self):
        assert False



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ModelCreateViewSetTestCases(
    TenancyMixinInheritedCases,
    CommonModelCreateViewSetInheritedCases,
):

    pass

class ModelCreateViewSetInherited(
    ModelCreateViewSetTestCases,
):

    pass

class TenancyPermissionsModelCreateViewSetPyTest(
    ModelCreateViewSetTestCases,
):
    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelCreateViewSet

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
        pytest.xfail( reason = 'base class is abstract with no model' )

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
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'


        assert view_set.get_serializer_class() == model_serializer['view']



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ModelListRetrieveDeleteViewSetTestCases(
    TenancyMixinInheritedCases,
    CommonModelListRetrieveDeleteViewSetInheritedCases,
):

    pass

class ModelListRetrieveDeleteViewSetInheritedCases(
    ModelListRetrieveDeleteViewSetTestCases,
):

    pass

class TenancyPermissionsModelListRetrieveDeleteViewSetPyTest(
    ModelListRetrieveDeleteViewSetTestCases,
):
    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelListRetrieveDeleteViewSet

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
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'


        assert view_set.get_serializer_class() == model_serializer['view']



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ModelRetrieveUpdateViewSetTestCases(
    TenancyMixinInheritedCases,
    CommonModelRetrieveUpdateViewSetInheritedCases,
):

    pass

class ModelRetrieveUpdateViewSetInheritedCases(
    ModelRetrieveUpdateViewSetTestCases,
):

    pass

class TenancyPermissionsModelRetrieveUpdateViewSetPyTest(
    ModelRetrieveUpdateViewSetTestCases,
):
    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelRetrieveUpdateViewSet

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



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class SubModelViewSetTestCases(
    TenancyMixinInheritedCases,
    CommonSubModelViewSetTestCases,
):
    pass

class SubModelViewSetInheritedCases(
    CommonSubModelViewSetInheritedCases,
    SubModelViewSetTestCases,
):
    pass

class TenancyPermissionsSubModelViewSetPyTest(
    SubModelViewSetTestCases,
):
    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return SubModelViewSet

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
            'base_model': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': NOT_USED,
                'value': NOT_USED
            },
            'model_suffix': {
                'type': type(None),
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'model_kwarg': {
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



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ReadOnlyModelViewSetTestCases(
    TenancyMixinInheritedCases,
    CommonReadOnlyModelViewSetInheritedCases,
):
    pass

class ReadOnlyModelViewSetInheritedCases(
    ReadOnlyModelViewSetTestCases,
):
    pass

class TenancyPermissionsReadOnlyModelViewSetPyTest(
    ReadOnlyModelViewSetTestCases,
):
    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ReadOnlyModelViewSet

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
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'


        assert view_set.get_serializer_class() == model_serializer['view']



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ReadOnlyListModelViewSetTestCases(
    TenancyMixinInheritedCases,
    CommonReadOnlyListModelViewSetInheritedCases,
):
    pass

class ReadOnlyListModelViewSetInheritedCases(
    ReadOnlyListModelViewSetTestCases,
):
    pass

class TenancyPermissionsReadOnlyListModelViewSetPyTest(
    ReadOnlyListModelViewSetTestCases,
):
    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ReadOnlyListModelViewSet

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
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'


        assert view_set.get_serializer_class() == model_serializer['view']
