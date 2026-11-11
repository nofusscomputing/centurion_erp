from django.db.models.base import ValidationError
import pytest

from django.db import models

from core.tests.unit.mixin_centurion.test_unit_centurion_mixin import CenturionMixnInheritedCases


@pytest.mark.model_itassetrelationships
class ITAssetRelationshipModelModelTestCases(
    CenturionMixnInheritedCases
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
                'value': False
            },
            'model_tag': {
                'type': type(None),
            },
        }



    def test_function_clean_fields_child_model_matches_relationship_model_valid(self,
        model, model_kwargs,
        model_itasset, kwargs_itasset
    ):
        """Test model function

        When clean_fields is called, if the child asset is set, validate that
        the child model matches the relationship model.
        """

        kwargs = kwargs_itasset()

        asset = model_itasset.objects.create( **kwargs )

        kwargs = model_kwargs()

        kwargs['child_asset_model'] = asset.device_model

        kwargs['child'] = asset

        test_model = model( **kwargs )

        test_model.clean_fields()

        assert test_model.child.device_model == test_model.child_asset_model



    def test_function_clean_fields_empty_relationship_child_model(self,
        model, model_kwargs,
        model_itasset, kwargs_itasset
    ):
        """Test model function

        When clean_fields is called, if the child asset is set, Raise no exceptions
        if there is no relationship child model.
        """

        kwargs = kwargs_itasset()

        asset = model_itasset.objects.create( **kwargs )

        kwargs = model_kwargs()

        # kwargs['child_asset_model'] = asset.device_model

        kwargs['child'] = asset

        test_model = model( **kwargs )

        test_model.clean_fields()

        assert test_model.child.device_model != test_model.child_asset_model



    def test_function_clean_fields_child_model_different_relationship_child_model(self,
        model, model_kwargs,
        model_itasset, kwargs_itasset
    ):
        """Test model function

        When clean_fields is called, if the child asset is set, raise an
        exception when the child model does not match the relationship child model.
        """

        kwargs = kwargs_itasset()

        asset = model_itasset.objects.create( **kwargs )


        kwargs = model_kwargs()

        kwargs['child_asset_model'] = kwargs_itasset()['device_model']

        kwargs['child'] = asset

        test_model = model( **kwargs )

        assert test_model.child.device_model != test_model.child_asset_model, \
            'Test cant continue if the models are the same.'

        with pytest.raises(ValidationError):

            test_model.clean_fields()



    @pytest.mark.xfail( reason = 'model is an M2M model and should not have model_tag defined.' )
    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None



    @pytest.mark.xfail( reason = 'Model requires additional kwargs.' )
    def test_method_get_url_kwargs(self, mocker, model_instance, settings):

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == { 'pk': model_instance.id }



    def test_method_get_url_kwargs_itassetrelationship(self, model_instance):

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'model_id': str(model_instance.parent_asset_model.id),
            'model_name': model_instance.parent_asset_model._meta.model_name,
            'related_model_name': 'connections',
            'pk': model_instance.id
        }



    @pytest.mark.xfail( reason = 'Model is m2m model and not setup to be audited.' )
    def test_method_get_audit_values_clean_model_returns_fields_only(self, mocker, model, model_instance):
        """Test Class Method
        
        Ensure method `get_audit_values` returns All model fields as a dict
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is abstract. Test is N/A.' )

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        for field in self.kwargs_create_item:

            if type(self.kwargs_create_item[field]) is list:
                continue

            setattr(model_instance, field, self.kwargs_create_item[field])


        m2m_fields = {}
        for m2m_field in model_instance._meta.many_to_many:

            value = list(
                getattr(model_instance, m2m_field.name).values_list(
                    'pk', flat = True
                )
            )

            if len(value) < 1:
                value = None

            m2m_fields.update({
                m2m_field.name: value
            })


        remaining_fields = {}
        for field in model_instance._meta.fields:

            value = getattr(model_instance, field.name, None)
            if(
                # field in self.kwargs_create_item
                # or value is not None
                # and field.name not in [ 'id', 'created', 'modified', 'organization' ]
                field.auto_created
            ):
                continue

            if isinstance(field, models.DateTimeField):
                if value and type(value) is not str:
                    value = value.isoformat(timespec='seconds')

            remaining_fields.update({
                field.name: value
            })


        method_values = model_instance.get_audit_values()

        assert method_values == {
            **m2m_fields,
            **remaining_fields,
        }    # Correct Values Returned

        assert len(method_values) == len([
                *[field for field in model_instance._meta.fields if not field.auto_created],    # Dont include parent model ptr
                *model_instance._meta.many_to_many
            ])
        # Fail-Safe to ensure test writer fills all fields



    @pytest.mark.xfail( reason = 'Model is m2m model and does not use this field.' )
    def test_method_value_not_default___str__(self, model, model_instance ):
        """Test Method

        Ensure method `__str__` does not return the default value.
        """

        if model._meta.abstract:

            pytest.xfail(reason = 'Model is an abstract model')


        default_value = f'{model_instance._meta.object_name} object ({str(model_instance.id)})'

        assert model_instance.__str__() != default_value



class ITAssetRelationshipModelModelInheritedCases(
    ITAssetRelationshipModelModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetRelationshipModelModelPyTest(
    ITAssetRelationshipModelModelTestCases,
):
    pass
