import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



# class Old:

#     model = ConfigGroupSoftware


#     @classmethod
#     def setUpTestData(self):
#         """ Setup Test

#         """

#         self.organization = Organization.objects.create(name='test_org')


#         self.parent_item = ConfigGroups.objects.create(
#             organization = self.organization,
#             name = 'group_one'
#         )

#         self.software_item = Software.objects.create(
#             organization = self.organization,
#             name = 'softwareone',
#         )

#         self.kwargs_item_create = {
#             'software': self.software_item,
#             'config_group': self.parent_item,
#             'action': DeviceSoftware.Actions.INSTALL
#         }

#         super().setUpTestData()



#     def test_model_has_property_parent_object(self):
#         """ Check if model contains 'parent_object'
        
#             This is a required property for all models that have a parent
#         """

#         assert hasattr(self.model, 'parent_object')


#     def test_model_property_parent_object_returns_object(self):
#         """ Check if model contains 'parent_object'
        
#             This is a required property for all models that have a parent
#         """

#         assert self.item.parent_object == self.parent_item



@pytest.mark.model_configgroupsoftware
class ConfigGroupSoftwareModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_notes_enabled': {
                'value': False,
            },
            '_ticket_linkable': {
                'value': False,
            },
            'model_tag': {
                'type': models.NOT_PROVIDED,
                'value': models.NOT_PROVIDED,
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
        'config_group': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'software': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'action': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': True,
            'unique': False,
        },
        'version': {
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


    @pytest.mark.xfail( reason = 'not required for this model' )
    def test_method_value_not_default___str__(self):
        pass

    @pytest.mark.xfail( reason = 'not required for this model' )
    def test_model_tag_defined(self):
        pass

    def test_method_get_url_kwargs(self, mocker, model_instance, model_kwargs, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == { 'config_group_id': model_kwargs['config_group'].id, 'pk': model_instance.id }



class ConfigGroupSoftwareModelInheritedCases(
    ConfigGroupSoftwareModelTestCases,
):
    pass



@pytest.mark.module_config_management
class ConfigGroupSoftwareModelPyTest(
    ConfigGroupSoftwareModelTestCases,
):
    pass
