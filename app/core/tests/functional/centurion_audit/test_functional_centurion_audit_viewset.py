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

