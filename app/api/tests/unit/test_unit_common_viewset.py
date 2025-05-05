import pytest

from django.contrib.auth.models import ContentType, Permission, User
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
from access.models.organization import Organization
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

    def __init__(self, user: User, organization: Organization, viewset):

        self.user = user

        if not isinstance(viewset, viewset):

            viewset = viewset()

        view_permission = Permission.objects.get(
            codename = 'view_' + viewset.model._meta.model_name,
            content_type = ContentType.objects.get(
                app_label = viewset.model._meta.app_label,
                model = viewset.model._meta.model_name,
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

    viewset = Create


    def test_class_inherits_viewsets_mixins_createmodel_mixin(self):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.CreateModelMixin`
        """

        assert issubclass(self.viewset, viewsets.mixins.CreateModelMixin)


    def test_view_attr_create_exists(self):
        """Attribute Test

        Function `create` must exist
        """

        assert hasattr(self.viewset, 'create')


    def test_view_attr_create_is_callable(self):
        """Attribute Test

        attribute `create` is callable / is a Function
        """

        view_set = self.viewset()

        assert callable(view_set.create)



class CreateTest(
    CreateCases,
    TestCase,
):

    pass


class DestroyCases:

    viewset = Destroy


    def test_class_inherits_viewsets_mixins_destroymodel_mixin(self):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.DestroyModelMixin`
        """

        assert issubclass(self.viewset, viewsets.mixins.DestroyModelMixin)


    def test_view_attr_destroy_exists(self):
        """Attribute Test

        Function `destroy` must exist
        """

        assert hasattr(self.viewset, 'destroy')


    def test_view_attr_destroy_is_callable(self):
        """Attribute Test

        attribute `destroy` is callable / is a Function
        """

        view_set = self.viewset()

        assert callable(view_set.destroy)



class DestroyTest(
    DestroyCases,
    TestCase,
):

    pass


class ListCases:

    viewset = List


    def test_class_inherits_viewsets_mixins_listmodel_mixin(self):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.ListModelMixin`
        """

        assert issubclass(self.viewset, viewsets.mixins.ListModelMixin)


    def test_view_attr_list_exists(self):
        """Attribute Test

        Function `list` must exist
        """

        assert hasattr(self.viewset, 'list')


    def test_view_attr_list_is_callable(self):
        """Attribute Test

        attribute `list` is callable / is a Function
        """

        view_set = self.viewset()

        assert callable(view_set.list)



class ListTest(
    ListCases,
    TestCase,
):

    pass



class RetrieveCases:

    viewset = Retrieve


    def test_class_inherits_viewsets_mixins_retrievemodel_mixin(self):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.RetrieveModelMixin`
        """

        assert issubclass(self.viewset, viewsets.mixins.RetrieveModelMixin)


    def test_view_attr_retrieve_exists(self):
        """Attribute Test

        Function `retrieve` must exist
        """

        assert hasattr(self.viewset, 'retrieve')


    def test_view_attr_retrieve_is_callable(self):
        """Attribute Test

        attribute `retrieve` is callable / is a Function
        """

        view_set = self.viewset()

        assert callable(view_set.retrieve)



class RetrieveTest(
    RetrieveCases,
    TestCase,
):

    pass



class UpdateCases:

    viewset = Update


    def test_class_inherits_viewsets_mixins_updatemodel_mixin(self):
        """Class Inheritence check

        Class must inherit from `viewsets.mixins.UpdateModelMixin`
        """

        assert issubclass(self.viewset, viewsets.mixins.UpdateModelMixin)


    def test_view_attr_partial_update_exists(self):
        """Attribute Test

        Function `partial_update` must exist
        """

        assert hasattr(self.viewset, 'partial_update')


    def test_view_attr_partial_update_is_callable(self):
        """Attribute Test

        attribute `partial_update` is callable / is a Function
        """

        view_set = self.viewset()

        assert callable(view_set.partial_update)


    def test_view_attr_update_exists(self):
        """Attribute Test

        Function `update` must exist
        """

        assert hasattr(self.viewset, 'update')


    def test_view_attr_update_is_callable(self):
        """Attribute Test

        attribute `update` is callable / is a Function
        """

        view_set = self.viewset()

        assert callable(view_set.update)



class UpdateTest(
    UpdateCases,
    TestCase,
):

    pass



class CommonViewSetCases(
    # OrganizationMixinTest,    # ToDo: Add `OrganizationMixin` test suit
):
    """Test Suite for class CommonViewSet"""


    viewset = CommonViewSet


    @classmethod
    def setUpTestData(self):

        self.kwargs: dict = {}

        if self.viewset is CommonViewSet:

            self.viewset.model = Organization


    def test_class_inherits_organizationmixin(self):
        """Class Inheritence check

        Class must inherit from `OrganizationMixin`
        """

        assert issubclass(self.viewset, OrganizationMixin)


    def test_class_inherits_viewsets_viewset(self):
        """Class Inheritence check

        Class must inherit from `viewsets.ViewSet`
        """

        assert issubclass(self.viewset, viewsets.ViewSet)



    def test_view_attr_allowed_methods_exists(self):
        """Attribute Test

        Attribute `allowed_methods` must exist
        """

        assert hasattr(self.viewset, 'allowed_methods')


    def test_view_attr_allowed_methods_not_empty(self):
        """Attribute Test

        Attribute `allowed_methods` must return a value
        """

        view_set = self.viewset()

        view_set.kwargs = self.kwargs

        assert view_set.allowed_methods is not None


    def test_view_attr_allowed_methods_type(self):
        """Attribute Test

        Attribute `allowed_methods` must be of type list
        """

        view_set = self.viewset()

        view_set.kwargs = self.kwargs

        assert type(view_set.allowed_methods) is list


    def test_view_attr_allowed_methods_values(self):
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

        view_set = self.viewset()

        for method in list(view_set.allowed_methods):

            if method not in valid_values:

                all_valid = False

        assert all_valid


    # ToDo: back_url


    def test_view_attr_documentation_exists(self):
        """Attribute Test

        Attribute `documentation` must exist
        """

        assert hasattr(self.viewset, 'documentation')


    def test_view_attr_documentation_type(self):
        """Attribute Test

        Attribute `documentation` must be of type str or None.

        this attribute is optional.
        """

        view_set = self.viewset()

        assert (
            type(view_set.documentation) is str
            or view_set.documentation is None
        )


    def test_view_attr_metadata_class_exists(self):
        """Attribute Test

        Attribute `metadata_class` must exist
        """

        assert hasattr(self.viewset, 'metadata_class')


    def test_view_attr_metadata_class_not_empty(self):
        """Attribute Test

        Attribute `metadata_class` must return a value
        """

        view_set = self.viewset()

        assert view_set.metadata_class is not None


    def test_view_attr_metadata_class_type(self):
        """Attribute Test

        Attribute `metadata_class` must be metadata class `ReactUIMetadata`
        """

        view_set = self.viewset()

        assert view_set.metadata_class is ReactUIMetadata


    # ToDo: metadata_markdown

    # ToDo: _model_documentation

    # ToDo: model_documentation

    # ToDo: page_layout

    def test_view_attr_permission_classes_exists(self):
        """Attribute Test

        Attribute `permission_classes` must exist
        """

        assert hasattr(self.viewset, 'permission_classes')


    def test_view_attr_permission_classes_not_empty(self):
        """Attribute Test

        Attribute `permission_classes` must return a value
        """

        view_set = self.viewset()

        assert view_set.permission_classes is not None


    def test_view_attr_permission_classes_type(self):
        """Attribute Test

        Attribute `permission_classes` must be list
        """

        view_set = self.viewset()

        assert type(view_set.permission_classes) is list


    def test_view_attr_permission_classes_value(self):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `ReactUIMetadata`
        """

        view_set = self.viewset()

        assert view_set.permission_classes[0] is OrganizationPermissionMixin

        assert len(view_set.permission_classes) == 1


    # ToDo: table_fields


    def test_view_attr_view_description_exists(self):
        """Attribute Test

        Attribute `view_description` must exist
        """

        assert hasattr(self.viewset, 'view_description')


    def test_view_attr_view_description_type(self):
        """Attribute Test

        Attribute `view_description` must be of type str if defined or None otherwise
        """

        assert(
            type(self.viewset.view_description) is str
            or type(self.viewset.view_description) is type(None)
        )


    def test_view_attr_view_name_exists(self):
        """Attribute Test

        Attribute `view_name` must exist
        """

        assert hasattr(self.viewset, 'view_name')


    def test_view_attr_view_name_type(self):
        """Attribute Test

        Attribute `view_name` must be of type str if defined or None otherwise
        """

        view_set = self.viewset()

        assert(
            type(view_set.view_name) is str
            or type(view_set.view_name) is type(None)
        )


    # ToDo: get_back_url

    # ToDo: get_model_documentation

    # ToDo: get_page_layout

    # ToDo: get_return_url

    # ToDo: get_table_fields

    # ToDo: get_view_description

    # ToDo: get_view_name



class CommonViewSetTest(
    CommonViewSetCases,
    TestCase,
):

    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class CommonViewSetAPIRenderOptionsCases:
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

    kwargs: dict = {}

    organization: Organization

    view_user: User

    viewset = ModelViewSetBase

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()    # Sets attribute self.view_set.model

        self.organization = Organization.objects.create(name='test_org')

        self.view_user = User.objects.create_user(username="test_view_user", password="password", is_superuser=True)


    def test_class_inherits_modelviewsetbase(self):
        """Class Inheritence check

        Class must inherit from `ModelViewSetBase`
        """

        assert issubclass(self.viewset, CommonViewSet)


    def test_view_attr_filterset_fields_exists(self):
        """Attribute Test

        Attribute `filterset_fields` must exist
        """

        assert hasattr(self.viewset, 'filterset_fields')


    def test_view_attr_filterset_fields_not_empty(self):
        """Attribute Test

        Attribute `filterset_fields` must return a value
        """

        assert self.viewset.filterset_fields is not None


    def test_view_attr_filterset_fields_type(self):
        """Attribute Test

        Attribute `filterset_fields` must be of type list
        """

        view_set = self.viewset()

        assert (
            type(view_set.filterset_fields) is list
        )



    def test_view_attr_lookup_value_regex_exists(self):
        """Attribute Test

        Attribute `lookup_value_regex` must exist
        """

        assert hasattr(self.viewset, 'lookup_value_regex')


    def test_view_attr_lookup_value_regex_not_empty(self):
        """Attribute Test

        Attribute `lookup_value_regex` must return a value
        """

        assert self.viewset.lookup_value_regex is not None


    def test_view_attr_lookup_value_regex_type(self):
        """Attribute Test

        Attribute `lookup_value_regex` must be of type list
        """

        view_set = self.viewset()

        assert (
            type(view_set.lookup_value_regex) is str
        )


    def test_view_attr_lookup_value_regex_value(self):
        """Attribute Test

        Attribute `lookup_value_regex` must have a value of `[0-9]+` as this
        is used for the PK lookup which is always a number.
        """

        view_set = self.viewset()

        assert view_set.lookup_value_regex == '[0-9]+'



    def test_view_attr_model_exists(self):
        """Attribute Test

        Attribute `model` must exist
        """

        assert hasattr(self.viewset, 'model')


    def test_view_attr_model_not_empty(self):
        """Attribute Test

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is not None


    # ToDo: queryset


    def test_view_attr_search_fields_exists(self):
        """Attribute Test

        Attribute `search_fields` must exist
        """

        assert hasattr(self.viewset, 'search_fields')


    def test_view_attr_search_fields_not_empty(self):
        """Attribute Test

        Attribute `search_fields` must return a value
        """

        assert self.viewset.search_fields is not None


    def test_view_attr_search_fields_type(self):
        """Attribute Test

        Attribute `search_fields` must be of type list
        """

        view_set = self.viewset()

        assert (
            type(view_set.search_fields) is list
        )


    # ToDo: serializer_class


    # ToDo: view_serializer_name


    def test_view_func_get_queryset_cache_result(self):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        view_set = self.viewset()

        view_set.request = MockRequest(
            user = self.view_user,
            organization = self.organization,
            viewset = self.viewset
        )

        view_set.request.headers = {}

        view_set.kwargs = self.kwargs

        view_set.action = 'list'

        view_set.detail = False

        assert view_set.queryset is None    # Must be empty before init

        q = view_set.get_queryset()

        assert view_set.queryset is not None    # Must not be empty after init

        assert q == view_set.queryset


    def test_view_func_get_queryset_cache_result_used(self):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        view_set = self.viewset()

        view_set.request = MockRequest(
            user = self.view_user,
            organization = self.organization,
            viewset = self.viewset
        )

        view_set.request.headers = {}
        view_set.kwargs = self.kwargs
        view_set.action = 'list'
        view_set.detail = False

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



class ModelViewSetBaseTest(
    ModelViewSetBaseCases,
    TestCase
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



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

    viewset = ModelViewSet



    def test_view_attr_allowed_methods_values(self):
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

        view_set = self.viewset()

        view_set.kwargs = self.kwargs

        for method in list(view_set.allowed_methods):

            if method not in valid_values:

                all_valid = False

        assert all_valid



    def test_class_inherits_modelviewsetbase(self):
        """Class Inheritence check

        Class must inherit from `ModelViewSetBase`
        """

        assert issubclass(self.viewset, ModelViewSetBase)


    def test_class_inherits_create(self):
        """Class Inheritence check

        Class must inherit from `Create`
        """

        assert issubclass(self.viewset, Create)


    def test_class_inherits_retrieve(self):
        """Class Inheritence check

        Class must inherit from `Retrieve`
        """

        assert issubclass(self.viewset, Retrieve)


    def test_class_inherits_update(self):
        """Class Inheritence check

        Class must inherit from `Update`
        """

        assert issubclass(self.viewset, Update)


    def test_class_inherits_destroy(self):
        """Class Inheritence check

        Class must inherit from `Destroy`
        """

        assert issubclass(self.viewset, Destroy)


    def test_class_inherits_list(self):
        """Class Inheritence check

        Class must inherit from `List`
        """

        assert issubclass(self.viewset, List)


    def test_class_inherits_viewsets_modelviewset(self):
        """Class Inheritence check

        Class must inherit from `viewsets.ModelViewSet`
        """

        assert issubclass(self.viewset, viewsets.ModelViewSet)



class ModelViewSetTest(
    ModelViewSetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class SubModelViewSetTestCases(
    ModelViewSetCases
):

    kwargs: dict

    organization: Organization

    view_user: User

    viewset = SubModelViewSet


    def test_class_inherits_submodelviewsetbase(self):
        """Class Inheritence check

        Class must inherit from `SubModelViewSet`
        """

        assert issubclass(self.viewset, SubModelViewSet)


    def test_view_attr_exists_base_model(self):
        """Attribute Test

        Attribute `base_model` must exist
        """

        assert hasattr(self.viewset, 'base_model')


    def test_view_attr_type_base_model(self):
        """Attribute Test

        Attribute `base_model` must be of type Django Model
        """

        view_set = self.viewset()

        assert issubclass(view_set.base_model, models.Model)



    def test_view_attr_exists_model_kwarg(self):
        """Attribute Test

        Attribute `model_kwarg` must exist
        """

        assert hasattr(self.viewset, 'model_kwarg')


    def test_view_attr_type_model_kwarg(self):
        """Attribute Test

        Attribute `model_kwarg` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.model_kwarg) is str



    def test_view_attr_value_model_kwarg(self):
        """Attribute Test

        Attribute `model_kwarg` must be equal to model._meta.sub_model_type
        """

        view_set = self.viewset()

        assert view_set.model_kwarg is not None



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



class SubModelViewSetTest(
    SubModelViewSetTestCases,
    TestCase,
):


    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None



    def test_view_attr_type_base_model(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `base_model` must be of type Django Model
        """

        assert True


    def test_view_attr_type_model_kwarg(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model_kwarg` must be of type str
        """

        view_set = self.viewset()

        assert view_set.model_kwarg is None


    def test_view_attr_value_model_kwarg(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model_kwarg` must be equal to model._meta.sub_model_type
        """

        view_set = self.viewset()

        assert view_set.model_kwarg is None

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

    viewset = ModelCreateViewSet


    def test_class_inherits_viewsets_genericviewset(self):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(self.viewset, viewsets.GenericViewSet)



class ModelCreateViewSetTest(
    ModelCreateViewSetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class ModelListRetrieveDeleteViewSetCases(
    ModelViewSetBaseCases,
    ListCases,
    RetrieveCases,
    DestroyCases,
):
    """Test Suite for class ModelListRetrieveDeleteViewSet"""

    viewset = ModelListRetrieveDeleteViewSet


    def test_class_inherits_viewsets_genericviewset(self):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(self.viewset, viewsets.GenericViewSet)



class ModelListRetrieveDeleteViewSetTest(
    ModelListRetrieveDeleteViewSetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class ModelRetrieveUpdateViewSetCases(
    ModelViewSetBaseCases,
    RetrieveCases,
    UpdateCases,
):
    """Test Suite for class ModelRetrieveUpdateViewSet"""

    viewset = ModelRetrieveUpdateViewSet


    def test_class_inherits_viewsets_genericviewset(self):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(self.viewset, viewsets.GenericViewSet)



class ModelRetrieveUpdateViewSetTest(
    ModelRetrieveUpdateViewSetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None


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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class ReadOnlyModelViewSetCases(
    ModelViewSetBaseCases,
    RetrieveCases,
    ListCases,
):
    """Test Suite for class ReadOnlyModelViewSet"""

    viewset = ReadOnlyModelViewSet


    def test_class_inherits_viewsets_genericviewset(self):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(self.viewset, viewsets.GenericViewSet)



class ReadOnlyModelViewSetTest(
    ReadOnlyModelViewSetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class ReadOnlyListModelViewSetCases(
    ModelViewSetBaseCases,
    ListCases,
):
    """Test Suite for class ReadOnlyListModelViewSet"""

    viewset = ReadOnlyListModelViewSet


    def test_class_inherits_viewsets_genericviewset(self):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(self.viewset, viewsets.GenericViewSet)



class ReadOnlyListModelViewSetTest(
    ReadOnlyListModelViewSetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class AuthUserReadOnlyModelViewSetCases(
    ReadOnlyModelViewSetCases,
):
    """Test Suite for class AuthUserReadOnlyModelViewSet"""

    viewset = AuthUserReadOnlyModelViewSet


    def test_view_attr_permission_classes_value(self):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `IsAuthenticated`
        """

        view_set = self.viewset()

        assert view_set.permission_classes[0] is IsAuthenticated

        assert len(view_set.permission_classes) == 1



class AuthUserReadOnlyModelViewSetTest(
    AuthUserReadOnlyModelViewSetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class IndexViewsetCases(
    ModelViewSetBaseCases,
):
    """Test Suite for class IndexViewset"""

    viewset = IndexViewset


    def test_view_attr_permission_classes_value(self):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `IsAuthenticated`
        """

        view_set = self.viewset()

        assert view_set.permission_classes[0] is IsAuthenticated

        assert len(view_set.permission_classes) == 1



class IndexViewsetTest(
    IndexViewsetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



class PublicReadOnlyViewSetCases(
    ReadOnlyListModelViewSetCases,
):
    """Test Suite for class PublicReadOnlyViewSet"""

    viewset = PublicReadOnlyViewSet


    def test_view_attr_metadata_class_type(self):
        """Attribute Test

        Attribute `metadata_class` must be metadata class `ReactUIMetadata`
        """

        view_set = self.viewset()

        assert view_set.metadata_class is JSONAPIMetadata


    def test_view_attr_permission_classes_value(self):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `IsAuthenticatedOrReadOnly`
        """

        view_set = self.viewset()

        assert view_set.permission_classes[0] is IsAuthenticatedOrReadOnly

        assert len(view_set.permission_classes) == 1



    def test_view_attr_pagination_class_exists(self):
        """Attribute Test

        Attribute `pagination_class` must exist
        """

        assert hasattr(self.viewset, 'pagination_class')


    def test_view_attr_pagination_class_not_empty(self):
        """Attribute Test

        Attribute `pagination_class` must return a value
        """

        view_set = self.viewset()

        assert view_set.pagination_class is not None


    def test_view_attr_pagination_class_type(self):
        """Attribute Test

        Attribute `pagination_class` must be of type StaticPageNumbering
        """

        view_set = self.viewset()

        assert view_set.pagination_class is StaticPageNumbering



class PublicReadOnlyViewSetTest(
    PublicReadOnlyViewSetCases,
    TestCase,
):

    def test_view_attr_model_not_empty(self):
        """Attribute Test

        This test case overrides a test case of the same name. As this test is
        checking the base classes, it's return is different to a class that
        has inherited from this or parent classes.

        Attribute `model` must return a value that is not None
        """

        view_set = self.viewset()

        assert view_set.model is None

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


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_description` must return a value that is not None
        """

        assert self.viewset.view_description is None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        As this Test Case is for the Base class this values type should be `None`

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is type(None)


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must return a value that is not None
        """

        assert self.viewset.view_name is None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        As this Test Case is for the Base class this value should be `None`

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert type(view_set.view_name) is type(None)



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
