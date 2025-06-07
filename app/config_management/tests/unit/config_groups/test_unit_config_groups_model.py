import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



class Old:

    kwargs_item_create = {
        'name': 'one',
        'config': dict({"key": "one", "existing": "dont_over_write"})
    }

    model = ConfigGroups

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        super().setUpTestData()


        self.second_item = self.model.objects.create(
            organization = self.organization,
            name = 'one_two',
            config = dict({"key": "two"}),
            parent = self.item
        )

    def test_config_groups_count_child_groups(self):
        """ Test function count_children """

        assert self.item.count_children() == 1


    def test_config_groups_rendered_config_not_empty(self):
        """ Rendered Config must be returned """

        assert self.item.config is not None


    def test_config_groups_rendered_config_is_dict(self):
        """ Rendered Config is a string """

        assert type(self.item.render_config()) is dict


    def test_config_groups_rendered_config_is_correct(self):
        """ Rendered Config is correct """

        assert self.item.config['key'] == 'one'


    def test_config_groups_rendered_config_inheritence_overwrite(self):
        """ rendered config from parent group merged correctly """

        assert self.second_item.config['key'] == 'two'


    def test_config_groups_rendered_config_inheritence_existing_key_present(self):
        """ rendered config from parent group merge existing key present
        
        during merge, a key that doesn't exist in the child group that exists in the
        parent group should be within the child groups rendered config
        """

        assert self.second_item.config['key'] == 'two'


    @pytest.mark.skip(reason="to be written")
    def test_config_groups_config_keys_valid_ansible_variable():
        """ All config keys must be valid ansible variables """
        pass



@pytest.mark.model_config_group
class ConfigGroupModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'config_group'
            },
        }


    parameterized_model_fields = {
        'parent': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'name': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'max_length': 50,
            'null': True,
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
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ManyToManyField,
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



class ConfigGroupModelInheritedCases(
    ConfigGroupModelTestCases,
):
    pass



class ConfigGroupModelPyTest(
    ConfigGroupModelTestCases,
):
    pass
