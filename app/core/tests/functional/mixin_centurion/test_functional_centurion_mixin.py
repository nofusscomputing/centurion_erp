import pytest

from centurion.tests.functional_models import ModelTestCases



@pytest.mark.mixin
@pytest.mark.mixin_centurion
class CenturionAbstractMixinTestCases(
    ModelTestCases
):


    def test_method_get_related_field_name_returns_parent_model_name(self,
        model, created_model
    ):
        """Test Class Method

        Test to ensure that when function `get_related_field_name` is called
        and the model is not the same as `._base_model`, it returns the name
        of the parent model as a string
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is abstract, test is N/A.' )

        if not model()._base_model or model()._base_model is model:
            pytest.xfail( reason = 'Not a sub-model, test is N/A.' )

        base_object = getattr(created_model, f'{model()._base_model._meta.model_name}_ptr')

        assert base_object.get_related_field_name() == created_model._meta.all_parents[0]._meta.model_name



    def test_method_get_related_model_returns_self(self,
        model, created_model
    ):
        """Test Class Method

        Test to ensure that when function `get_related_model` is called and
        and the model is not the same as `._base_model` or the related model
        is directly called, it returns self.

        Note: This function must work for ALL models, not just sub-models.
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is abstract, test is N/A.' )

        assert type(created_model.get_related_model()) is model



    def test_method_get_related_model_returns_model(self,
        model, created_model
    ):
        """Test Class Method

        Test to ensure that when function `get_related_model` is called and
        and the model is the `._base_model` it returns the correct model.
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is abstract, test is N/A.' )

        if not model()._base_model or model()._base_model is model:
            pytest.xfail( reason = 'Not a sub-model, test is N/A.' )

        base_object = getattr(created_model, f'{model()._base_model._meta.model_name}_ptr')

        assert type(base_object.get_related_model()) is model




class CenturionAbstractMixinInheritedCases(
    CenturionAbstractMixinTestCases,
):
    pass


@pytest.mark.module_core
class CenturionAbstractMixinPyTest(
    CenturionAbstractMixinTestCases,
):
    pass
