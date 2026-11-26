import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_itassetsoftware
class ITAssetSoftwareModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):



    def test_property_get_configuration_software_add(self,
        model, model_kwargs,
    ):
        """ Test model property

        Ensure that property `get_configuration` returns the correct value.
        """

        the_model = model.objects.create( **model_kwargs() )

        asset = the_model.it_asset

        software = {
            'software': [
                {
                    'name': the_model.software.name,
                    'state': 'present',
                    'version': the_model.version.name
                }
            ]
        }

        assert asset.get_configuration == {
            **asset.config,
            **software
        }



    def test_property_get_configuration_software_remove(self,
        model, model_kwargs,
    ):
        """ Test model property

        Ensure that property `get_configuration` returns the correct value.
        """

        the_model = model.objects.create( **model_kwargs() )

        the_model.action = 0

        the_model.save()

        asset = the_model.it_asset

        software = {
            'software': [
                {
                    'name': the_model.software.name,
                    'state': 'absent',
                    'version': the_model.version.name
                }
            ]
        }

        assert asset.get_configuration == {
            **asset.config,
            **software
        }



class ITAssetSoftwareModelInheritedCases(
    ITAssetSoftwareModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetSoftwareModelPyTest(
    ITAssetSoftwareModelTestCases,
):
    pass
