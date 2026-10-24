import pytest

from django.db import models

from accounting.tests.unit.asset_base.test_unit_asset_base_model import (
    AssetBaseModelInheritedCases,
    AssetBase
)

from itam.models import ITAssetSoftware
from itam.tests.unit.itam_asset_base.test_unit_itam_asset_base_model  import (
    ITAMAssetModelInheritedCases
)



@pytest.mark.model_itassetsoftware
class ITAssetSoftwareModelTestCases(
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
                'value': 'software'
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
            'category': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            'modified': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateTimeField,
                'null': False,
                'unique': False,
            },
        }


    def test_class_inherits_itassetsoftware(self, model):
        """ Class inheritence

        Model Must Inherit from itassetsoftware
        """

        assert issubclass(model, ITAssetSoftware)



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'model has its own stringify convention' )
    def test_function__str__has_asset_number(self,
        model, model_kwargs,
    ):
        """Test model function
        
        Ensure that if asset_number exists that it is used in model
        stringify.
        """

        test_model = model( **model_kwargs() )

        assert str(test_model).endswith(test_model.asset_number)



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'model has its own stringify convention' )
    def test_function__str__no_asset_number(self,
        model, model_kwargs,
    ):
        """Test model function
        
        Ensure that if there is not asset_number that it is not used in model
        stringify.
        """

        kwargs = model_kwargs()
        del kwargs['asset_number']

        test_model = model( **kwargs )

        assert test_model._meta.verbose_name == str(test_model)



class ITAssetSoftwareModelInheritedCases(
    ITAssetSoftwareModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetSoftwareModelPyTest(
    ITAssetSoftwareModelTestCases,
):
    pass
