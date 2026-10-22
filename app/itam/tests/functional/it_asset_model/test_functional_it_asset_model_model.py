import pytest
import re

from django.core.exceptions import ValidationError

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_model import (
    ITAMAssetBaseModelInheritedCases
)



@pytest.mark.model_itassetmodel
class ITAssetModelModelTestCases(
    ITAMAssetBaseModelInheritedCases
):
    pass



class ITAssetModelModelInheritedCases(
    ITAssetModelModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelModelPyTest(
    ITAssetModelModelTestCases,
):
    pass
