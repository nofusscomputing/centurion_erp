from django.db import models

from accounting.tests.unit.asset_base.test_unit_asset_base_model import AssetBaseModelInheritedCases

from itam.models.itam_asset_base import ITAMAssetBase



class ITAMAssetBaseModelTestCases(
    AssetBaseModelInheritedCases,
):

    kwargs_create_item: dict = {}

    sub_model_type = 'itam_base'
    """Sub Model Type
    
    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """


    parameterized_fields: dict = {
        "itam_type": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': ITAMAssetBase._meta.itam_sub_model_type,
            'field_parameter_verbose_name_type': str
        }
    }



    def test_class_inherits_itam_assetbase(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, ITAMAssetBase)



    def test_attribute_type_app_namespace(self):
        """Attribute Type

        app_namespace is of type str
        """

        assert self.model.app_namespace is None


    def test_attribute_value_app_namespace(self):
        """Attribute Type

        app_namespace has been set, override this test case with the value
        of attribute `app_namespace`
        """

        assert self.model.app_namespace is None



class ITAMAssetBaseModelInheritedCases(
    ITAMAssetBaseModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model AssetBase
    """

    kwargs_create_item: dict = {}

    model = None


    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """



class ITAMAssetBaseModelPyTest(
    ITAMAssetBaseModelTestCases,
):

    pass
