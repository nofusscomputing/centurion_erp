import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_assetbase
class AssetBaseModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class AssetBaseModelInheritedCases(
    AssetBaseModelTestCases,
):
    pass



@pytest.mark.module_accounting
class AssetBaseModelPyTest(
    AssetBaseModelTestCases,
):
    pass
