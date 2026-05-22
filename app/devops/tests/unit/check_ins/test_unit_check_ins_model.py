import pytest

from django.db import models

from pytest_simplified import NOT_USED

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_checkin
class CheckInModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'value': False
            },
            '_notes_enabled': {
                'value': False
            },
            '_ticket_linkable': {
                'value': False,
            },
            'model_tag': {
                'type': NOT_USED,
                'value': NOT_USED
            },
            'app_namespace': {
                'type': str,
                'value': 'public:devops'
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
        'model_notes': {
            'blank': models.fields.NOT_PROVIDED,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.fields.NOT_PROVIDED,
            'null': models.fields.NOT_PROVIDED,
            'unique': models.fields.NOT_PROVIDED,
        },
        'software': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'version': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'length': 80,
            'null': True,
            'unique': False,
        },
        'deployment_id': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 30,
            'null': False,
            'unique': False,
        },
        'feature': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'null': False,
            'unique': False,
        }
    }



class CheckInModelInheritedCases(
    CheckInModelTestCases,
):
    pass



@pytest.mark.module_devops
class CheckInModelPyTest(
    CheckInModelTestCases,
):

    @pytest.mark.xfail( reason = 'model does not need tag' )
    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None


    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'organization_id': model_instance.organization.id,
            'software_id': model_instance.software.id
        }

    def test_attribute_page_layout_table_fields(self):
        pytest.xfail( reason = 'This model has no endpoint' )

    def test_attribute_page_layout_dataset_columns_fields(self):
        pytest.xfail( reason = 'This model has no endpoint' )

    def test_attribute_page_layout_detail_section_columns(self):
        pytest.xfail( reason = 'This model has no endpoint' )
