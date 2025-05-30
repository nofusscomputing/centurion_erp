import pytest

from django.db import models

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_feature_flag
class FeatureFlagModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @pytest.fixture( scope = 'class', autouse = True )
    def software_setup(self, request, django_db_blocker, organization_one):

        from itam.models.software import Software

        with django_db_blocker.unblock():

            software = Software.objects.create(
                organization = organization_one,
                name = 'software test'
            )

        request.cls.kwargs_create_item.update({
            'software': software
        })

        yield

        with django_db_blocker.unblock():

            software.delete()



    kwargs_create_item = {
            'software': None,
            'name': 'a name',
            'description': ' a description',
            'enabled': True,
        }



    @property
    def parameterized_class_attributes(self):

        return {
            'is_global': {
                'type': type(None),
                'value': None,
            },
            'model_tag': {
                'type': str,
                'value': 'feature_flag'
            },
        }


    parameterized_model_fields = {
        'software': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': False,
            'unique': False,
        },
        'description': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'null': True,
            'unique': False,
        },
        'enabled': {
            'blank': False,
            'default': False,
            'field_type': models.BooleanField,
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



class FeatureFlagModelInheritedCases(
    FeatureFlagModelTestCases,
):
    pass



class FeatureFlagModelPyTest(
    FeatureFlagModelTestCases,
):
    pass
