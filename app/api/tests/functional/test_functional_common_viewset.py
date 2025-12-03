import django
import pytest
import random

from django.contrib.auth.models import ContentType, Group, Permission

from access.models.tenant import Tenant
from access.models.role import Role
from api.viewsets.common.common import (
    Create,
    Destroy,
    List,
    Retrieve,
    Update,

    ModelViewSetBase,

    CommonViewSet,
    CommonModelViewSet,
    CommonSubModelViewSet_ReWrite,

    CommonModelCreateViewSet,
    CommonModelListRetrieveDeleteViewSet,
    CommonModelRetrieveUpdateViewSet,
    CommonReadOnlyModelViewSet,
    CommonReadOnlyListModelViewSet,
)

from settings.models.app_settings import AppSettings

User = django.contrib.auth.get_user_model()



class MockRequest:
    """Fake Request

    contains the user and tenancy object for permission checks

    Some ViewSets rely upon the request object for obtaining the user and
    fetching the tenacy object for permission checking.
    """

    data = {}

    kwargs = {}

    user: User = None

    def __init__(self, user: User, tenant: Tenant, viewset, model = None):

        self.user = user

        if not isinstance(viewset, viewset):

            viewset = viewset()

        if model is None:

            model = viewset.model

        view_permission = Permission.objects.get(
            codename = 'view_' + model._meta.model_name,
            content_type = ContentType.objects.get(
                app_label = model._meta.app_label,
                model = model._meta.model_name,
            )
        )

        view_group = Group.objects.create(
            name = 'view_team',
        )

        view_role = Role.objects.create(
            name = 'view_role',
            organization = tenant,
        )

        view_group.roles.set( [view_role] )

        view_role.permissions.set([view_permission])

        user.groups.set([ view_group ])


        self.app_settings = AppSettings.objects.select_related('global_organization').get(
            owner_organization = None
        )



@pytest.mark.api
@pytest.mark.viewset
@pytest.mark.functional
class CreateCases:
    pass


class CommonCreatePyTest(
    CreateCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Create



@pytest.mark.api
@pytest.mark.viewset
@pytest.mark.functional
class DestroyCases:
    pass


class CommonDestroyPyTest(
    DestroyCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Destroy



@pytest.mark.api
@pytest.mark.viewset
@pytest.mark.functional
class ListCases:
    pass


class CommonListPyTest(
    ListCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return List



@pytest.mark.api
@pytest.mark.viewset
@pytest.mark.functional
class RetrieveCases:
    pass


class CommonRetrievePyTest(
    RetrieveCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Retrieve



@pytest.mark.api
@pytest.mark.viewset
@pytest.mark.functional
class UpdateCases:
    pass


class CommonUpdatePyTest(
    UpdateCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Update



@pytest.mark.api
@pytest.mark.viewset
@pytest.mark.functional
class CommonViewSetTestCases:
    """Test Suite for class CommonViewSet"""

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        clean_model_from_db, api_request_permissions,
        model_user, kwargs_user, organization_one, organization_two,
        model_instance, model_kwargs, model, model_ticketcommentbase
    ):

        with django_db_blocker.unblock():

            user = api_request_permissions['user']['view']

            kwargs = kwargs_user()
            kwargs['username'] = 'username.two' + str(
                random.randint(1,99) + random.randint(1,99) + random.randint(1,99) )
            user2 = model_user.objects.create( **kwargs )

            self.user = user

            kwargs = model_kwargs()
            if 'organization' in kwargs:
                kwargs['organization'] = organization_one
            if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
                kwargs['user'] = user2
            user_tenancy_item = model_instance( kwargs_create = kwargs )

            kwargs = model_kwargs()
            if 'organization' in kwargs:
                kwargs['organization'] = organization_two
            if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
                kwargs['user'] = user
            other_tenancy_item = model_instance( kwargs_create = kwargs )

        view_set = viewset()
        view_set.kwargs = user_tenancy_item.get_url_kwargs( many = True )
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


        yield view_set

        del view_set.request
        del view_set
        del self.user

        clean_model_from_db(model)
        clean_model_from_db(model_user)



    # parmeterize to view action
    def test_function_get_queryset_filtered_results_action_list(self,
        viewset_mock_request, organization_one, organization_two, model
    ):
        """Test class function

        Ensure that when function `get_queryset` returns values that are filtered
        """

        viewset = viewset_mock_request

        viewset.action = 'list'

        if not viewset.model:
            pytest.xfail( reason = 'no model exists, assuming viewset is a base/mixin viewset.' )

        only_user_results_returned = True

        for permission_class in viewset.permission_classes:
            viewset.permissions_required = permission_class().get_required_permissions(
            method = 'GET',
            model_cls = model
        )

        queryset = viewset.get_queryset()

        assert len(model.objects.all()) >= 2, 'multiple objects must exist for test to work'
        assert len( queryset ) > 0, 'Empty queryset returned. Test not possible'
        if model._meta.model_name != 'tenant':
            assert len(model.objects.filter( organization = organization_one)) > 0, 'objects in user org required for test to work.'
            assert len(model.objects.filter( organization = organization_two)) > 0, 'objects in different org required for test to work.'


        for result in queryset:

            if result.get_tenant() != organization_one:
                only_user_results_returned = False

        assert only_user_results_returned



class CommonViewSetPyTest(
    CommonViewSetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



@pytest.mark.api
@pytest.mark.viewset
@pytest.mark.functional
class ModelViewSetBaseCases(
    CommonViewSetTestCases,
):
    pass


class CommonModelViewSetBasePyTest(
    ModelViewSetBaseCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelViewSetBase

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



class ModelViewSetTestCases(
    ModelViewSetBaseCases,
    CreateCases,
    RetrieveCases,
    UpdateCases,
    DestroyCases,
    ListCases,
):
    pass


class CommonModelViewSetPyTest(
    ModelViewSetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonModelViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



class CommonSubModelViewSetTestCases(
    ModelViewSetTestCases
):
    pass


class CommonSubModelViewSetPyTest(
    CommonSubModelViewSetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonSubModelViewSet_ReWrite

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



class ModelCreateViewSetTestCases(
    ModelViewSetBaseCases,
    CreateCases,
):
    pass


class CommonModelCreateViewSetPyTest(
    ModelCreateViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonModelCreateViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



class ModelListRetrieveDeleteViewSetTestCases(
    ModelViewSetBaseCases,
    ListCases,
    RetrieveCases,
    DestroyCases,
):
    pass


class CommonModelListRetrieveDeleteViewSetPyTest(
    ModelListRetrieveDeleteViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonModelListRetrieveDeleteViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



class ModelRetrieveUpdateViewSetTestCases(
    ModelViewSetBaseCases,
    RetrieveCases,
    UpdateCases,
):
    pass


class CommonModelRetrieveUpdateViewSetPyTest(
    ModelRetrieveUpdateViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonModelRetrieveUpdateViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



class ReadOnlyModelViewSetTestCases(
    ModelViewSetBaseCases,
    RetrieveCases,
    ListCases,
):
    pass


class CommonReadOnlyModelViewSetPyTest(
    ReadOnlyModelViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonReadOnlyModelViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )



class ReadOnlyListModelViewSetTestCases(
    ModelViewSetBaseCases,
    ListCases,
):
    pass

class CommonReadOnlyListModelViewSetPyTest(
    ReadOnlyListModelViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonReadOnlyListModelViewSet

    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'Base class does not require test' )




#########################################################################################
#
#    Use the below test cases for Viewset that inherit the class `(.+)InheritedCases`
#
#########################################################################################



class CommonModelCreateViewSetInheritedCases(
    ModelCreateViewSetTestCases,
):

    pass



class CommonModelListRetrieveDeleteViewSetInheritedCases(
    ModelListRetrieveDeleteViewSetTestCases,
):

    pass



class CommonModelRetrieveUpdateViewSetInheritedCases(
    ModelRetrieveUpdateViewSetTestCases,
):

    pass



class CommonModelViewSetInheritedCases(
    ModelViewSetTestCases,
):
    pass


class CommonSubModelViewSetInheritedCases(
    CommonSubModelViewSetTestCases,
):
    pass


class CommonReadOnlyListModelViewSetInheritedCases(
    ReadOnlyListModelViewSetTestCases,
):
    pass

class CommonReadOnlyModelViewSetInheritedCases(
    ReadOnlyModelViewSetTestCases,
):

    pass
