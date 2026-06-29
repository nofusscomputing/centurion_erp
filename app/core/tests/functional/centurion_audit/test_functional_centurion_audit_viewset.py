import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases
)

from core.viewsets.audit_history import (
    ViewSet,
)



@pytest.mark.model_centurionaudit
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class CenturionAuditViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class CenturionAuditViewsetPyTest(
    ViewsetTestCases,
):

    def test_function_get_meta_urls_no_sub_models_key(self):
        pytest.xfail( reason = 'Base class does not require test' )

    def test_function_get_meta_urls_sub_models_keys(self):
        pytest.xfail( reason = 'Model is not creatable by user so sub_models not required.' )

    def test_function_get_meta_urls_sub_models_values(self):
        pytest.xfail( reason = 'Model is not creatable by user so sub_models not required.' )
