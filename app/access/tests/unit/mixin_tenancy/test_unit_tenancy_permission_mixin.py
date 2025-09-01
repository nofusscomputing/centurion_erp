import pytest

from access.permissions.tenancy import TenancyPermissions

from centurion.tests.unit_class import ClassTestCases



@pytest.mark.mixin
@pytest.mark.mixin_tenancy
class TenancyMixinTestCases(
    ClassTestCases
):



    @property
    def parameterized_class_attributes(self):

        return {
            '_obj_tenancy': {
                'type': type(None),
                'value': None
            },
            '_queryset': {
                'type': type(None),
                'value': None
            },
            'parent_model': {
                'type': type(None),
                'value': None
            },
            'parent_model_pk_kwarg': {
                'type': str,
                'value': 'pk'
            },
            'permission_classes': {
                'type': list,
                'value': [ TenancyPermissions ]
            },
            '_obj_tenancy': {
                'type': type(None),
                'value': None
            },
        }


    def test_function_get_parent_model(self, mocker, viewset):
        """Test class function

        Ensure that when function `get_parent_model` is called it returns the value
        of `viewset.parent_model`
        """

        viewset_instance = viewset()
        mocker.patch.object(viewset_instance, 'parent_model', 'fred' )

        assert viewset_instance.get_parent_model() == 'fred'



    # queryset does cache



class TenancyMixinInheritedCases(
    TenancyMixinTestCases
):

    def test_function_get_parent_model(self, mocker, viewset):
        """Test class function

        Ensure that when function `get_parent_model` is called it returns the value
        of `viewset.parent_model`.

        For all models that dont have attribute `viewset.parent_model` set, it should
        return None
        """

        assert viewset().get_parent_model() is None




@pytest.mark.module_access
class TenancyMixinPyTest(
    TenancyMixinTestCases
):

    @pytest.fixture
    def test_class(self, mixin):
        return mixin
