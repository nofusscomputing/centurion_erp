import pytest

from api.tests.functional.test_functional_common_viewset import MockRequest
from api.tests.functional.viewset.test_functional_user_viewset import (
    ModelRetrieveUpdateViewSetInheritedCases
)

from settings.viewsets.user_settings import (
    ViewSet,
)



@pytest.mark.model_usersettings
class ViewsetTestCases(
    ModelRetrieveUpdateViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        model_user, kwargs_user, organization_one, organization_two,
        model_instance, model_kwargs, model
    ):

        with django_db_blocker.unblock():

            user = model_user.objects.create( **kwargs_user() )

            kwargs = kwargs_user()
            kwargs['username'] = 'username.two'
            user2 = model_user.objects.create( **kwargs )

            self.user = user

            user_tenancy_item = model.objects.get(
                user = user
            )

            other_tenancy_item = model.objects.get(
                user = user2
            )

        view_set = viewset()
        model = getattr(view_set, 'model', None)

        if not model:
            model = Tenant

        request = MockRequest(
            user = user,
            model = model,
            viewset = viewset,
            tenant = organization_one
        )

        view_set.request = request
        view_set.kwargs = user_tenancy_item.get_url_kwargs( many = True )


        yield view_set

        del view_set.request
        del view_set
        del self.user

        with django_db_blocker.unblock():

            for group in user.groups.all():

                for role in group.roles.all():
                    role.delete()

                group.delete()

            # user_tenancy_item.delete()
            # other_tenancy_item.delete()

            user.delete()
            user2.delete



class UserSettingsViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_settings
class UserSettingsViewsetPyTest(
    ViewsetTestCases,
):

    pass
