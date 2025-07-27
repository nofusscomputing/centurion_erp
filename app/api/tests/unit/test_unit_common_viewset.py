import django
import pytest

from django.contrib.auth.models import ContentType, Permission
from django.db import models
from django.test import TestCase

from unittest.mock import patch, PropertyMock

from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly,
)
from rest_framework_json_api.metadata import JSONAPIMetadata

from access.middleware.request import Tenancy
from access.mixins.organization import OrganizationMixin
from access.mixins.permissions import OrganizationPermissionMixin
from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.react_ui_metadata import ReactUIMetadata
from api.viewsets.common import (
    Create,
    Destroy,
    List,
    Retrieve,
    Update,

    ModelViewSetBase,
    StaticPageNumbering,

    CommonViewSet,
    ModelViewSet,
    SubModelViewSet,

    ModelCreateViewSet,
    ModelListRetrieveDeleteViewSet,
    ModelRetrieveUpdateViewSet,
    ReadOnlyModelViewSet,
    ReadOnlyListModelViewSet,
    AuthUserReadOnlyModelViewSet,
    IndexViewset,
    PublicReadOnlyViewSet,
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

    tenancy: Tenancy = None

    user: User = None

    def __init__(self, user: User, organization: Organization, viewset, model = None):

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

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permission])


        TeamUsers.objects.create(
            team = view_team,
            user = user
        )


        self.app_settings = AppSettings.objects.select_related('global_organization').get(
            owner_organization = None
        )

        self.tenancy = Tenancy(
            user = user,
            app_settings = self.app_settings
        )



class CreateCases:


    def test_class_inherits_viewsets_mixins_createmodel_mixin(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.CreateModelMixin`
        """

        assert issubclass(viewset, viewsets.mixins.CreateModelMixin)


    def test_view_attr_create_exists(self, viewset):
        """Attribute Test

        Function `create` must exist
        """

        assert hasattr(viewset, 'create')


    def test_view_attr_create_is_callable(self, viewset):
        """Attribute Test

        attribute `create` is callable / is a Function
        """

        assert callable(viewset().create)



@pytest.mark.api
@pytest.mark.viewset
class CreatePyTest(
    CreateCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Create



class DestroyCases:


    def test_class_inherits_viewsets_mixins_destroymodel_mixin(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.DestroyModelMixin`
        """

        assert issubclass(viewset, viewsets.mixins.DestroyModelMixin)


    def test_view_attr_destroy_exists(self, viewset):
        """Attribute Test

        Function `destroy` must exist
        """

        assert hasattr(viewset, 'destroy')


    def test_view_attr_destroy_is_callable(self, viewset):
        """Attribute Test

        attribute `destroy` is callable / is a Function
        """

        assert callable(viewset().destroy)



@pytest.mark.api
@pytest.mark.viewset
class DestroyPyTest(
    DestroyCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Destroy



class ListCases:


    def test_class_inherits_viewsets_mixins_listmodel_mixin(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.ListModelMixin`
        """

        assert issubclass(viewset, viewsets.mixins.ListModelMixin)


    def test_view_attr_list_exists(self, viewset):
        """Attribute Test

        Function `list` must exist
        """

        assert hasattr(viewset, 'list')


    def test_view_attr_list_is_callable(self, viewset):
        """Attribute Test

        attribute `list` is callable / is a Function
        """

        assert callable(viewset().list)



@pytest.mark.api
@pytest.mark.viewset
class ListPyTest(
    ListCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return List



class RetrieveCases:


    def test_class_inherits_viewsets_mixins_retrievemodel_mixin(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.RetrieveModelMixin`
        """

        assert issubclass(viewset, viewsets.mixins.RetrieveModelMixin)


    def test_view_attr_retrieve_exists(self, viewset):
        """Attribute Test

        Function `retrieve` must exist
        """

        assert hasattr(viewset, 'retrieve')


    def test_view_attr_retrieve_is_callable(self, viewset):
        """Attribute Test

        attribute `retrieve` is callable / is a Function
        """

        assert callable(viewset().retrieve)



@pytest.mark.api
@pytest.mark.viewset
class RetrievePyTest(
    RetrieveCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Retrieve



class UpdateCases:


    def test_class_inherits_viewsets_mixins_updatemodel_mixin(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.UpdateModelMixin`
        """

        assert issubclass(viewset, viewsets.mixins.UpdateModelMixin)


    def test_view_attr_partial_update_exists(self, viewset):
        """Attribute Test

        Function `partial_update` must exist
        """

        assert hasattr(viewset, 'partial_update')


    def test_view_attr_partial_update_is_callable(self, viewset):
        """Attribute Test

        attribute `partial_update` is callable / is a Function
        """

        assert callable(viewset().partial_update)


    def test_view_attr_update_exists(self, viewset):
        """Attribute Test

        Function `update` must exist
        """

        assert hasattr(viewset, 'update')


    def test_view_attr_update_is_callable(self, viewset):
        """Attribute Test

        attribute `update` is callable / is a Function
        """

        assert callable(viewset().update)



@pytest.mark.api
@pytest.mark.viewset
class UpdatePyTest(
    UpdateCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Update




class CommonViewSetCases(
    # OrganizationMixinTest,    # ToDo: Add `OrganizationMixin` test suit
):
    """Test Suite for class CommonViewSet"""

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, viewset):

        request = MockRequest(
            user = self.view_user,
            model = getattr(self, 'model',None),
            viewset = self.viewset,
            organization = self.organization
        )

        view_set = viewset()
        view_set.request = request

        yield view_set

        del view_set.request


    # @classmethod
    # def setUpTestData(self):

    #     self.kwargs: dict = {}

    #     if self.viewset is CommonViewSet:

    #         self.viewset.model = Organization


    def test_class_inherits_organizationmixin(self, viewset):
        """Class Inheritence check

        Class must inherit from `OrganizationMixin`
        """

        assert issubclass(viewset, OrganizationMixin)


    def test_class_inherits_viewsets_viewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.ViewSet`
        """

        assert issubclass(viewset, viewsets.ViewSet)



    def test_view_attr_allowed_methods_exists(self, viewset):
        """Attribute Test

        Attribute `allowed_methods` must exist
        """

        assert hasattr(viewset, 'allowed_methods')


    def test_view_attr_allowed_methods_not_empty(self, viewset):
        """Attribute Test

        Attribute `allowed_methods` must return a value
        """

        assert viewset.allowed_methods is not None


    def test_view_attr_allowed_methods_type(self, viewset):
        """Attribute Test

        Attribute `allowed_methods` must be of type list
        """

        assert type(viewset().allowed_methods) is list


    def test_view_attr_allowed_methods_values(self, viewset):
        """Attribute Test

        Attribute `allowed_methods` only contains valid values
        """

        # Values valid for index views
        valid_values: list = [
            'GET',
            'HEAD',
            'OPTIONS',
        ]

        all_valid: bool = True

        for method in list(viewset().allowed_methods):

            if method not in valid_values:

                all_valid = False

        assert all_valid


    # ToDo: back_url


    def test_view_attr_documentation_exists(self, viewset):
        """Attribute Test

        Attribute `documentation` must exist
        """

        assert hasattr(viewset, 'documentation')


    def test_view_attr_documentation_type(self, viewset):
        """Attribute Test

        Attribute `documentation` must be of type str or None.

        this attribute is optional.
        """

        assert (
            type(viewset.documentation) is str
            or viewset.documentation is None
        )


    def test_view_attr_metadata_class_exists(self, viewset):
        """Attribute Test

        Attribute `metadata_class` must exist
        """

        assert hasattr(viewset, 'metadata_class')


    def test_view_attr_metadata_class_not_empty(self, viewset):
        """Attribute Test

        Attribute `metadata_class` must return a value
        """

        assert viewset.metadata_class is not None


    def test_view_attr_metadata_class_type(self, viewset):
        """Attribute Test

        Attribute `metadata_class` must be metadata class `ReactUIMetadata`
        """

        assert viewset.metadata_class is ReactUIMetadata


    # ToDo: metadata_markdown

    # ToDo: _model_documentation

    # ToDo: model_documentation

    # ToDo: page_layout

    def test_view_attr_permission_classes_exists(self, viewset):
        """Attribute Test

        Attribute `permission_classes` must exist
        """

        assert hasattr(viewset, 'permission_classes')


    def test_view_attr_permission_classes_not_empty(self, viewset):
        """Attribute Test

        Attribute `permission_classes` must return a value
        """

        assert viewset.permission_classes is not None


    def test_view_attr_permission_classes_type(self, viewset):
        """Attribute Test

        Attribute `permission_classes` must be list
        """

        assert type(viewset.permission_classes) is list


    def test_view_attr_permission_classes_value(self, viewset):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `ReactUIMetadata`
        """

        assert viewset.permission_classes[0] is OrganizationPermissionMixin

        assert len(viewset.permission_classes) == 1


    # ToDo: table_fields


    def test_view_attr_view_description_exists(self, viewset):
        """Attribute Test

        Attribute `view_description` must exist
        """

        assert hasattr(viewset, 'view_description')


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        Attribute `view_description` must be of type str if defined or None otherwise
        """

        assert(
            type(viewset.view_description) is str
            or type(viewset.view_description) is type(None)
        )


    def test_view_attr_view_name_exists(self, viewset):
        """Attribute Test

        Attribute `view_name` must exist
        """

        assert hasattr(viewset, 'view_name')


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        Attribute `view_name` must be of type str if defined or None otherwise
        """

        assert(
            type(viewset.view_name) is str
            or type(viewset.view_name) is type(None)
        )


    # ToDo: get_back_url

    # ToDo: get_model_documentation

    # ToDo: get_page_layout

    # ToDo: get_return_url

    # ToDo: get_table_fields

    # ToDo: get_view_description

    # ToDo: get_view_name



@pytest.mark.api
@pytest.mark.viewset
class CommonViewSetPyTest(
    CommonViewSetCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonViewSet


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset.view_name) is type(None)



class CommonViewSetAPIRenderOptionsCases:    # ToDo
    """Test Cases for ViewSets that inherit from CommonViewSet
    
    Dont Include this test suite directy, use the test cases below `*InheritedTest`
    """

    http_options_response_list = None
    """Inherited class must make and store here a HTTP/Options request"""


    def test_api_render_field_allowed_methods_exists(self):
        """Attribute Test

        Attribute `allowed_methods` must exist
        """

        assert 'allowed_methods' in self.http_options_response_list.data


    def test_api_render_field_allowed_methods_not_empty(self):
        """Attribute Test

        Attribute `allowed_methods` must return a value
        """

        assert len(self.http_options_response_list.data['allowed_methods']) > 0


    def test_api_render_field_allowed_methods_type(self):
        """Attribute Test

        Attribute `allowed_methods` must be of type list
        """

        assert type(self.http_options_response_list.data['allowed_methods']) is list


    def test_api_render_field_allowed_methods_values(self):
        """Attribute Test

        Attribute `allowed_methods` only contains valid values
        """

        # Values valid for index views
        valid_values: list = [
            'GET',
            'HEAD',
            'OPTIONS',
        ]

        all_valid: bool = True

        for method in list(self.http_options_response_list.data['allowed_methods']):

            if method not in valid_values:

                all_valid = False

        assert all_valid



    def test_api_render_field_view_description_exists(self):
        """Attribute Test

        Attribute `description` must exist
        """

        assert 'description' in self.http_options_response_list.data


    def test_api_render_field_view_description_not_empty(self):
        """Attribute Test

        Attribute `view_description` must return a value
        """

        assert self.http_options_response_list.data['description'] is not None


    def test_api_render_field_view_description_type(self):
        """Attribute Test

        Attribute `view_description` must be of type str
        """

        assert type(self.http_options_response_list.data['description']) is str



    def test_api_render_field_view_name_exists(self):
        """Attribute Test

        Attribute `view_name` must exist
        """

        assert 'name' in self.http_options_response_list.data


    def test_api_render_field_view_name_not_empty(self):
        """Attribute Test

        Attribute `view_name` must return a value
        """

        assert self.http_options_response_list.data['name'] is not None


    def test_api_render_field_view_name_type(self):
        """Attribute Test

        Attribute `view_name` must be of type str
        """

        assert type(self.http_options_response_list.data['name']) is str



class ModelViewSetBaseCases(
    CommonViewSetCases,
):
    """Test Suite for class ModelViewSetBase"""

    # kwargs: dict = {}

    # organization: Organization

    # view_user: User

    # @classmethod
    # def setUpTestData(self):

    #     super().setUpTestData()    # Sets attribute self.view_set.model

    #     self.organization = Organization.objects.create(name='test_org')

    #     self.view_user = User.objects.create_user(username="test_view_user1278", password="password", is_superuser=True)


    #     @classmethod
    #     def tearDownClass(cls):

    #         cls.model = None

    #         cls.organization.delete()

    #         cls.view_user.delete()

    #         super().tearDownClass()


    def test_class_inherits_modelviewsetbase(self, viewset):
        """Class Inheritence check

        Class must inherit from `ModelViewSetBase`
        """

        assert issubclass(viewset, CommonViewSet)


    def test_view_attr_filterset_fields_exists(self, viewset):
        """Attribute Test

        Attribute `filterset_fields` must exist
        """

        assert hasattr(viewset, 'filterset_fields')


    def test_view_attr_filterset_fields_not_empty(self, viewset):
        """Attribute Test

        Attribute `filterset_fields` must return a value
        """

        assert viewset.filterset_fields is not None


    def test_view_attr_filterset_fields_type(self, viewset):
        """Attribute Test

        Attribute `filterset_fields` must be of type list
        """

        assert (
            type(viewset().filterset_fields) is list
        )



    def test_view_attr_lookup_value_regex_exists(self, viewset):
        """Attribute Test

        Attribute `lookup_value_regex` must exist
        """

        assert hasattr(viewset, 'lookup_value_regex')


    def test_view_attr_lookup_value_regex_not_empty(self, viewset):
        """Attribute Test

        Attribute `lookup_value_regex` must return a value
        """

        assert viewset.lookup_value_regex is not None


    def test_view_attr_lookup_value_regex_type(self, viewset):
        """Attribute Test

        Attribute `lookup_value_regex` must be of type list
        """

        assert (
            type(viewset().lookup_value_regex) is str
        )


    def test_view_attr_lookup_value_regex_value(self, viewset):
        """Attribute Test

        Attribute `lookup_value_regex` must have a value of `[0-9]+` as this
        is used for the PK lookup which is always a number.
        """

        assert viewset().lookup_value_regex == '[0-9]+'



    def test_view_attr_model_exists(self, viewset):
        """Attribute Test

        Attribute `model` must exist
        """

        assert hasattr(viewset, 'model')


    def test_view_attr_model_not_empty(self, viewset_mock_request):
        """Attribute Test

        Attribute `model` must return a value that is not None
        """

        # view_set = self.viewset()
        # view_set.request = MockRequest(
        #     user = self.view_user,
        #     model = getattr(self, 'model',None),
        #     viewset = self.viewset,
        #     organization = self.organization
        # )

        assert viewset_mock_request.model is not None


    # ToDo: queryset


    def test_view_attr_search_fields_exists(self, viewset):
        """Attribute Test

        Attribute `search_fields` must exist
        """

        assert hasattr(viewset, 'search_fields')


    def test_view_attr_search_fields_not_empty(self, viewset):
        """Attribute Test

        Attribute `search_fields` must return a value
        """

        assert viewset.search_fields is not None


    def test_view_attr_search_fields_type(self, viewset):
        """Attribute Test

        Attribute `search_fields` must be of type list
        """

        assert (
            type(viewset().search_fields) is list
        )


    # ToDo: serializer_class


    # ToDo: view_serializer_name


    def test_view_func_get_queryset_cache_result(self, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        view_set = viewset_mock_request

        # view_set.request = MockRequest(
        #     user = self.view_user,
        #     model = getattr(self, 'model',None),
        #     organization = self.organization,
        #     viewset = self.viewset,
        # )

        # view_set.request.headers = {}

        # view_set.kwargs = self.kwargs

        # view_set.action = 'list'

        # view_set.detail = False

        assert view_set.queryset is None    # Must be empty before init

        q = view_set.get_queryset()

        assert view_set.queryset is not None    # Must not be empty after init

        assert q == view_set.queryset


    def test_view_func_get_queryset_cache_result_used(self, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        view_set = viewset_mock_request

        # view_set.request = MockRequest(
        #     user = self.view_user,
        #     model = getattr(self, 'model',None),
        #     organization = self.organization,
        #     viewset = self.viewset,
        # )

        # view_set.request.headers = {}
        # view_set.kwargs = self.kwargs
        # view_set.action = 'list'
        # view_set.detail = False

        mock_return = view_set.get_queryset()    # Real item to be used as mock return Some
                                                 # functions use `Queryset` for additional filtering

        setter_not_called = True


        with patch.object(self.viewset, 'queryset', new_callable=PropertyMock) as qs:

            qs.return_value = mock_return

            mocked_view_set = self.viewset()

            mocked_view_set.kwargs = self.kwargs
            mocked_view_set.action = 'list'
            mocked_view_set.detail = False

            qs.reset_mock()    # Just in case

            mocked_view_set.get_queryset()    # should only add two calls, if exists and the return


            for mock_call in list(qs.mock_calls):    # mock_calls with args means setter was called

                if len(mock_call.args) > 0:

                    setter_not_called = False


        assert setter_not_called
        assert qs.call_count == 2



@pytest.mark.api
@pytest.mark.viewset
class ModelViewSetBasePyTest(
    ModelViewSetBaseCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelViewSetBase


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self, viewset):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self, viewset):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class ModelViewSetCases(
    ModelViewSetBaseCases,
    CreateCases,
    RetrieveCases,
    UpdateCases,
    DestroyCases,
    ListCases,
):
    """Test Suite for class ModelViewSet
    
    Dont use inherit from this class use `ModelViewSetInheritedTest`
    """


    def test_view_attr_allowed_methods_values(self, viewset):
        """Attribute Test

        Attribute `allowed_methods` only contains valid values
        """

        # Values valid for model views
        valid_values: list = [
            'DELETE',
            'GET',
            'HEAD',
            'OPTIONS',
            'PATCH',
            'POST',
            'PUT',
        ]

        all_valid: bool = True

        # view_set = self.viewset()

        # view_set.kwargs = self.kwargs

        for method in list(viewset().allowed_methods):

            if method not in valid_values:

                all_valid = False

        assert all_valid



    def test_class_inherits_modelviewsetbase(self, viewset):
        """Class Inheritence check

        Class must inherit from `ModelViewSetBase`
        """

        assert issubclass(viewset, ModelViewSetBase)


    def test_class_inherits_create(self, viewset):
        """Class Inheritence check

        Class must inherit from `Create`
        """

        assert issubclass(viewset, Create)


    def test_class_inherits_retrieve(self, viewset):
        """Class Inheritence check

        Class must inherit from `Retrieve`
        """

        assert issubclass(viewset, Retrieve)


    def test_class_inherits_update(self, viewset):
        """Class Inheritence check

        Class must inherit from `Update`
        """

        assert issubclass(viewset, Update)


    def test_class_inherits_destroy(self, viewset):
        """Class Inheritence check

        Class must inherit from `Destroy`
        """

        assert issubclass(viewset, Destroy)


    def test_class_inherits_list(self, viewset):
        """Class Inheritence check

        Class must inherit from `List`
        """

        assert issubclass(viewset, List)


    def test_class_inherits_viewsets_modelviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.ModelViewSet`
        """

        assert issubclass(viewset, viewsets.ModelViewSet)



@pytest.mark.api
@pytest.mark.viewset
class ModelViewSetPyTest(
    ModelViewSetCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self, viewset):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self, viewset):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class SubModelViewSetTestCases(
    ModelViewSetCases
):

    # kwargs: dict

    # organization: Organization

    # view_user: User

    # viewset = SubModelViewSet


    def test_class_inherits_submodelviewsetbase(self, viewset):
        """Class Inheritence check

        Class must inherit from `SubModelViewSet`
        """

        assert issubclass(viewset, SubModelViewSet)


    def test_view_attr_exists_base_model(self, viewset):
        """Attribute Test

        Attribute `base_model` must exist
        """

        assert hasattr(viewset, 'base_model')


    def test_view_attr_type_base_model(self, viewset):
        """Attribute Test

        Attribute `base_model` must be of type Django Model
        """

        assert issubclass(viewset().base_model, models.Model)



    def test_view_attr_exists_model_kwarg(self, viewset):
        """Attribute Test

        Attribute `model_kwarg` must exist
        """

        assert hasattr(viewset, 'model_kwarg')


    def test_view_attr_type_model_kwarg(self, viewset):
        """Attribute Test

        Attribute `model_kwarg` must be of type str
        """

        assert type(viewset().model_kwarg) is str



    def test_view_attr_value_model_kwarg(self, viewset):
        """Attribute Test

        Attribute `model_kwarg` must be equal to model._meta.sub_model_type
        """

        assert viewset().model_kwarg is not None



    @pytest.mark.skip( reason = 'to be written')
    def test_view_func_related_objects(self):
        """ Function Test

        Function `related_objects` must return the highest model in the chain
        of models
        """

        pass



    @pytest.mark.skip( reason = 'to be written')
    def test_view_func_get_serializer_class_view(self):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        pass



    @pytest.mark.skip( reason = 'to be written')
    def test_view_func_get_serializer_class_create(self):
        """ Function Test

        Function `get_serializer_class` must return the correct create
        serializer for the model in question.
        """

        pass



@pytest.mark.api
@pytest.mark.viewset
class SubModelViewSetPyTest(
    SubModelViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return SubModelViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None



    def test_view_attr_type_base_model(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `base_model` must be of type Django Model
        """

        assert True


    def test_view_attr_type_model_kwarg(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model_kwarg` must be of type str
        """

        assert viewset().model_kwarg is None


    def test_view_attr_value_model_kwarg(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model_kwarg` must be equal to model._meta.sub_model_type
        """

        assert viewset().model_kwarg is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True



class ModelCreateViewSetCases(
    ModelViewSetBaseCases,
    CreateCases,
):
    """Test Suite for class ModelCreateViewSet"""

    def test_class_inherits_viewsets_genericviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(viewset, viewsets.GenericViewSet)



@pytest.mark.api
@pytest.mark.viewset
class ModelCreateViewSetPyTest(
    ModelCreateViewSetCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelCreateViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class ModelListRetrieveDeleteViewSetCases(
    ModelViewSetBaseCases,
    ListCases,
    RetrieveCases,
    DestroyCases,
):
    """Test Suite for class ModelListRetrieveDeleteViewSet"""

    viewset = ModelListRetrieveDeleteViewSet


    def test_class_inherits_viewsets_genericviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(viewset, viewsets.GenericViewSet)



@pytest.mark.api
@pytest.mark.viewset
class ModelListRetrieveDeleteViewSetPyTest(
    ModelListRetrieveDeleteViewSetCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelListRetrieveDeleteViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class ModelRetrieveUpdateViewSetCases(
    ModelViewSetBaseCases,
    RetrieveCases,
    UpdateCases,
):
    """Test Suite for class ModelRetrieveUpdateViewSet"""

    def test_class_inherits_viewsets_genericviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(viewset, viewsets.GenericViewSet)



@pytest.mark.api
@pytest.mark.viewset
class ModelRetrieveUpdateViewSetPyTest(
    ModelRetrieveUpdateViewSetCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelRetrieveUpdateViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None


    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class ReadOnlyModelViewSetCases(
    ModelViewSetBaseCases,
    RetrieveCases,
    ListCases,
):
    """Test Suite for class ReadOnlyModelViewSet"""


    def test_class_inherits_viewsets_genericviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(viewset, viewsets.GenericViewSet)



@pytest.mark.api
@pytest.mark.viewset
class ReadOnlyModelViewSetPyTest(
    ReadOnlyModelViewSetCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ReadOnlyModelViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class ReadOnlyListModelViewSetCases(
    ModelViewSetBaseCases,
    ListCases,
):
    """Test Suite for class ReadOnlyListModelViewSet"""


    def test_class_inherits_viewsets_genericviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(viewset, viewsets.GenericViewSet)



@pytest.mark.api
@pytest.mark.viewset
class ReadOnlyListModelViewSetPyTest(
    ReadOnlyListModelViewSetCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ReadOnlyListModelViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class AuthUserReadOnlyModelViewSetCases(
    ReadOnlyModelViewSetCases,
):
    """Test Suite for class AuthUserReadOnlyModelViewSet"""


    def test_view_attr_permission_classes_value(self, viewset):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `IsAuthenticated`
        """

        view_set = viewset()

        assert view_set.permission_classes[0] is IsAuthenticated

        assert len(view_set.permission_classes) == 1



@pytest.mark.api
@pytest.mark.viewset
class AuthUserReadOnlyModelViewSetPyTest(
    AuthUserReadOnlyModelViewSetCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return AuthUserReadOnlyModelViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class IndexViewsetCases(
    ModelViewSetBaseCases,
):
    """Test Suite for class IndexViewset"""

    viewset = IndexViewset


    def test_view_attr_permission_classes_value(self, viewset):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `IsAuthenticated`
        """

        assert viewset().permission_classes[0] is IsAuthenticated

        assert len(viewset().permission_classes) == 1



@pytest.mark.api
@pytest.mark.viewset
class IndexViewsetPyTest(
    IndexViewsetCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return IndexViewset


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



class PublicReadOnlyViewSetCases(
    ReadOnlyListModelViewSetCases,
):
    """Test Suite for class PublicReadOnlyViewSet"""

    viewset = PublicReadOnlyViewSet


    def test_view_attr_metadata_class_type(self, viewset):
        """Attribute Test

        Attribute `metadata_class` must be metadata class `ReactUIMetadata`
        """

        assert viewset().metadata_class is JSONAPIMetadata


    def test_view_attr_permission_classes_value(self, viewset):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `IsAuthenticatedOrReadOnly`
        """

        assert viewset().permission_classes[0] is IsAuthenticatedOrReadOnly

        assert len(viewset().permission_classes) == 1



    def test_view_attr_pagination_class_exists(self, viewset):
        """Attribute Test

        Attribute `pagination_class` must exist
        """

        assert hasattr(viewset, 'pagination_class')


    def test_view_attr_pagination_class_not_empty(self, viewset):
        """Attribute Test

        Attribute `pagination_class` must return a value
        """

        assert viewset().pagination_class is not None


    def test_view_attr_pagination_class_type(self, viewset):
        """Attribute Test

        Attribute `pagination_class` must be of type StaticPageNumbering
        """

        assert viewset().pagination_class is StaticPageNumbering



@pytest.mark.api
@pytest.mark.viewset
class PublicReadOnlyViewSetPyTest(
    PublicReadOnlyViewSetCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return PublicReadOnlyViewSet


    def test_view_attr_model_not_empty(self, viewset):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        assert viewset().model is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This test case overrides a test case of the same name. This test case
        is not required for this test suite.

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_attr_view_description_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert viewset.view_description is None


    def test_view_attr_view_description_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert viewset.view_name is None


    def test_view_attr_view_name_type(self, viewset):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        assert type(viewset().view_name) is type(None)



#########################################################################################
#
#    Use the below test cases for Viewset that inherit the class `(.+)InheritedCases`
#
#########################################################################################



class AuthUserReadOnlyModelViewSetInheritedCases(
    AuthUserReadOnlyModelViewSetCases,
):

    pass



class IndexViewsetInheritedCases(
    IndexViewsetCases,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This view does not use a model

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        This view does not use a queryset

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        This view does not use a queryset

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        assert True



class ModelCreateViewSetInheritedCases(
    ModelCreateViewSetCases,
):

    pass



class ModelListRetrieveDeleteViewSetInheritedCases(
    ModelListRetrieveDeleteViewSetCases,
):

    pass



class ModelRetrieveUpdateViewSetInheritedCases(
    ModelRetrieveUpdateViewSetCases,
):

    pass



class ModelViewSetInheritedCases(
    ModelViewSetCases,
    CommonViewSetAPIRenderOptionsCases,
):
    """Test Suite for classes that inherit ModelViewSet
    
    Use this Test Suite for ViewSet classes that inherit from ModelViewSet
    """

    http_options_response_list = None
    """Inherited class must make and store here a HTTP/Options request"""

    route_name = None
    """Inherited class must define the url rout name with namespace"""

    viewset = None


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is not None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is str


    def test_api_render_field_allowed_methods_values(self):
        """Attribute Test

        Attribute `allowed_methods` only contains valid values
        """

        # Values valid for model views
        valid_values: list = [
            'DELETE',
            'GET',
            'HEAD',
            'OPTIONS',
            'PATCH',
            'POST',
            'PUT',
        ]

        all_valid: bool = True

        for method in list(self.http_options_response_list.data['allowed_methods']):

            if method not in valid_values:

                all_valid = False

        assert all_valid



class SubModelViewSetInheritedCases(
    SubModelViewSetTestCases,
    CommonViewSetAPIRenderOptionsCases,
):
    """Test Suite for classes that inherit SubModelViewSet
    
    Use this Test Suite for ViewSet classes that inherit from SubModelViewSet
    """

    http_options_response_list = None
    """Inherited class must make and store here a HTTP/Options request"""

    route_name = None
    """Inherited class must define the url rout name with namespace"""

    base_model = None
    """The Sub Model that is returned from the model property"""

    viewset = None


    # @classmethod
    # def setUpTestData(self):
    #     """Setup Test

    #     1. make list request
    #     """

    #     self.viewset.kwargs = {}

    #     self.viewset.kwargs[self.viewset.model_kwarg] = self.model._meta.sub_model_type

    #     super().setUpTestData()



    def test_api_render_field_allowed_methods_values(self):
        """Attribute Test

        Attribute `allowed_methods` only contains valid values
        """

        # Values valid for model views
        valid_values: list = [
            'DELETE',
            'GET',
            'HEAD',
            'OPTIONS',
            'PATCH',
            'POST',
            'PUT',
        ]

        all_valid: bool = True

        for method in list(self.http_options_response_list.data['allowed_methods']):

            if method not in valid_values:

                all_valid = False

        assert all_valid


    def test_view_attr_model_value(self):
        """Attribute Test

        Attribute `model` must return the correct sub-model
        """

        view_set = self.viewset()

        assert view_set.model == self.model



class PublicReadOnlyViewSetInheritedCases(
    PublicReadOnlyViewSetCases,
):

    pass



class ReadOnlyModelViewSetInheritedCases(
    ReadOnlyModelViewSetCases,
):

    pass
