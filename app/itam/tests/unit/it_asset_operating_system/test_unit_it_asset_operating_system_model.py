import pytest

from django.db import models

from accounting.tests.unit.asset_base.test_unit_asset_base_model import (
    AssetBaseModelInheritedCases,
    AssetBase
)

from itam.models import ITAssetOperatingSystem
from itam.tests.unit.itam_asset_base.test_unit_itam_asset_base_model  import (
    ITAMAssetModelInheritedCases
)



@pytest.mark.model_itassetoperatingsystem
class ITAssetOperatingSystemModelTestCases(
    ITAMAssetModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': True
            },
            'app_namespace': {
                'type': str,
                'value': 'accounting'
            },
            'model_tag': {
                'type': str,
                'value': 'operating_system'
            },
            'url_model_name': {
                'type': str,
                'value': 'asset'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'publisher': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            'name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 50,
                'null': False,
                'unique': True,
            },
            'modified': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateTimeField,
                'null': False,
                'unique': False,
            },
        }


    def test_class_inherits_itassetoperatingsystem(self, model):
        """ Class inheritence

        Model Must Inherit from itassetoperatingsystem
        """

        assert issubclass(model, ITAssetOperatingSystem)



class ITAssetOperatingSystemModelInheritedCases(
    ITAssetOperatingSystemModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetOperatingSystemModelPyTest(
    ITAssetOperatingSystemModelTestCases,
):
    pass
