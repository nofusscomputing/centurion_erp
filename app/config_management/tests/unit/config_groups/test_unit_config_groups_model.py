import pytest

from django.db import models

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_configgroups
class ConfigGroupModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'config_group'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
        'parent': {
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
            'max_length': 50,
            'null': False,
            'unique': False,
        },
        'config': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.JSONField,
            'null': True,
            'unique': False,
        },
        'hosts': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ManyToManyField,
            'null': False,
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


#     def test_config_groups_count_child_groups(self):
#         """ Test function count_children """

#         assert self.item.count_children() == 1


#     def test_config_groups_rendered_config_not_empty(self):
#         """ Rendered Config must be returned """

#         assert self.item.config is not None


#     def test_config_groups_rendered_config_is_dict(self):
#         """ Rendered Config is a string """

#         assert type(self.item.render_config()) is dict


#     def test_config_groups_rendered_config_is_correct(self):
#         """ Rendered Config is correct """

#         assert self.item.config['key'] == 'one'


#     def test_config_groups_rendered_config_inheritence_overwrite(self):
#         """ rendered config from parent group merged correctly """

#         assert self.second_item.config['key'] == 'two'


#     def test_config_groups_rendered_config_inheritence_existing_key_present(self):
#         """ rendered config from parent group merge existing key present
        
#         during merge, a key that doesn't exist in the child group that exists in the
#         parent group should be within the child groups rendered config
#         """

#         assert self.second_item.config['key'] == 'two'


#     @pytest.mark.skip(reason="to be written")
#     def test_config_groups_config_keys_valid_ansible_variable():
#         """ All config keys must be valid ansible variables """
#         pass



class ConfigGroupModelInheritedCases(
    ConfigGroupModelTestCases,
):
    pass



@pytest.mark.module_config_management
class ConfigGroupModelPyTest(
    ConfigGroupModelTestCases,
):
    pass
