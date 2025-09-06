import django
import pytest

from access.tests.unit.mixin_tenancy.test_unit_tenancy_permission_mixin import (
    TenancyMixinInheritedCases
)

# from api.tests.unit.test_unit_common_viewset import (
#     CommonModelViewSetInheritedCases,
#     CommonModelCreateViewSetInheritedCases,
#     CommonModelListRetrieveDeleteViewSetInheritedCases,
#     CommonModelRetrieveUpdateViewSetInheritedCases,
#     CommonSubModelViewSetTestCases,
#     CommonSubModelViewSetInheritedCases,
#     CommonReadOnlyModelViewSetInheritedCases,
#     CommonReadOnlyListModelViewSetInheritedCases,

# )
from api.tests.functional.test_functional_common_viewset import (
    # CommonViewSetInheritedCases
    # CommonViewSetTestCases
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
    # TenancyMixinInheritedCases,
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

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ModelCreateViewSetTestCases(
    # TenancyMixinInheritedCases,
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

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ModelListRetrieveDeleteViewSetTestCases(
    # TenancyMixinInheritedCases,
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

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ModelRetrieveUpdateViewSetTestCases(
    # TenancyMixinInheritedCases,
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

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class SubModelViewSetTestCases(
    # TenancyMixinInheritedCases,
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

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ReadOnlyModelViewSetTestCases(
    # TenancyMixinInheritedCases,
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

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.permissions_tenancy
@pytest.mark.permissions
class ReadOnlyListModelViewSetTestCases(
    # TenancyMixinInheritedCases,
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

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )
