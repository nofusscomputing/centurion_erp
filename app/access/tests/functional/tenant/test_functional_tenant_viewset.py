import pytest

from access.viewsets.organization import (
    ViewSet,
)

from api.tests.functional.test_functional_common_viewset import MockRequest
from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases,
)



@pytest.mark.model_tenant
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        model_user, kwargs_user, organization_one, organization_two,
        model_instance, model_kwargs
    ):

        with django_db_blocker.unblock():

            user = model_user.objects.create( **kwargs_user )

            # kwargs = model_kwargs.copy()
            # kwargs['organization'] = organization_one
            user_tenancy_item = organization_one

            # kwargs = model_kwargs.copy()
            # kwargs['organization'] = organization_two
            other_tenancy_item = organization_two

        view_set = viewset()
        model = getattr(view_set, 'model', None)

        # if not model:
        #     model = Tenant

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

        with django_db_blocker.unblock():

            for group in user.groups.all():

                for role in group.roles.all():
                    role.delete()

                group.delete()

            user.delete()

            # user_tenancy_item.delete()
            # other_tenancy_item.delete()



class TenantViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class TenantViewsetPyTest(
    ViewsetTestCases,
):
    pass
