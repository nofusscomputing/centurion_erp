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



    def test_function_get_queryset_manager_calls_user(self, mocker, model, viewset):
        """Test class function

        Ensure that when function `get_queryset` the manager is first called with
        `.user()` so as to ensure that the queryset returns only data the user has
        access to.
        """

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs =  {}

        if model._is_submodel:
            view_set.kwargs =  {
                view_set.model_kwarg: model._meta.model_name
            }

        view_set.get_queryset()

        manager.user.assert_called()


    def test_function_get_queryset_manager_filters_by_pk(self, mocker, model, viewset):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `pk` kwarg
        """

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            'pk': 1
        }

        if model._is_submodel:
            view_set.kwargs.update({
                view_set.model_kwarg: model._meta.model_name
            })

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(pk=1)


    def test_function_get_queryset_manager_filters_by_model_id(self, mocker, model, viewset):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `.model_kwarg` kwarg
        """

        if not model._is_submodel:
            pytest.xfail( reason = 'test case only applicable to sub-models' )

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            'model_id': 1,
            view_set.model_kwarg: model._meta.model_name
        }

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(model_id=1)



@pytest.mark.module_access
class TenancyMixinPyTest(
    TenancyMixinTestCases
):

    @pytest.fixture
    def test_class(self, mixin):
        return mixin
