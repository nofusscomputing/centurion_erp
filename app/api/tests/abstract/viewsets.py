from django.contrib.auth.models import ContentType, Permission, User

from unittest.mock import patch, PropertyMock

from access.mixins.permissions import OrganizationPermissionMixin

from api.react_ui_metadata import ReactUIMetadata

from access.middleware.request import Tenancy
from access.models.organization import Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

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


        teamuser = TeamUsers.objects.create(
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



class AllViewSet:
    """Tests specific to the Viewset

    **Dont include these tests directly, see below for correct class**

    Tests are for ALL viewsets.
    """

    viewset = None
    """ViewSet to Test"""



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



    def test_view_attr_view_description_exists(self):
        """Attribute Test

        Attribute `view_description` must exist
        """

        assert hasattr(self.viewset, 'view_description')


    def test_view_attr_view_description_not_empty(self):
        """Attribute Test

        Attribute `view_description` must return a value
        """

        assert self.viewset.view_description is not None


    def test_view_attr_view_description_type(self):
        """Attribute Test

        Attribute `view_description` must be of type str
        """

        assert type(self.viewset.view_description) is str



    def test_view_attr_view_name_exists(self):
        """Attribute Test

        Attribute `view_name` must exist
        """

        assert hasattr(self.viewset, 'view_name')


    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        Attribute `view_name` must return a value
        """

        assert self.viewset.view_name is not None


    def test_view_attr_view_name_type(self):
        """Attribute Test

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert (
            type(view_set.view_name) is str
        )



class APIRenderViewSet:

    """Function ViewSet test

    **Dont include these tests directly, see below for correct class**

    These tests ensure that the data from the ViewSet is present for a 
    HTTP Request
    """

    http_options_response_list: dict = None
    """The HTTP/Options Response for the ViewSet"""



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



class ModelViewSet(AllViewSet):
    """Tests for Model Viewsets

    **Dont include these tests directly, see below for correct class**
    """

    viewset = None
    """ViewSet to Test"""



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



    def test_view_attr_model_exists(self):
        """Attribute Test

        Attribute `model` must exist
        """

        assert hasattr(self.viewset, 'model')


    def test_view_attr_model_not_empty(self):
        """Attribute Test

        Attribute `model` must return a value
        """

        view_set = self.viewset()

        assert view_set.model is not None



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



    def test_view_attr_view_name_not_empty(self):
        """Attribute Test

        Attribute `view_name` must return a value
        """

        view_set = self.viewset()

        assert (
            view_set.view_name is not None
            or view_set.get_view_name() is not None
        )


    def test_view_attr_view_name_type(self):
        """Attribute Test

        Attribute `view_name` must be of type str
        """

        view_set = self.viewset()

        assert (
            type(view_set.view_name) is str
            or type(view_set.get_view_name()) is str
        )



class APIRenderModelViewSet(APIRenderViewSet):
    """Tests for Model Viewsets

    **Dont include these tests directly, see below for correct class**
    """

    viewset = None
    """ViewSet to Test"""


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



class ViewSetCommon(
    AllViewSet,
    APIRenderViewSet
):
    """ Tests for Non-Model Viewsets

    **Include this class directly into Non-Model ViewSets**

    Args:
        AllViewSet (class): Tests for all Viewsets.
        APIRenderViewSet (class): Tests to check API Rendering to ensure data present.
    """
    pass


class ViewSetModel(
    ModelViewSet,
    APIRenderModelViewSet
):
    """Tests for model ViewSets

    **Include this class directly into Model ViewSets**

    Args:
        ModelViewSet (class): Tests for Model Viewsets, includes `AllViewSet` tests.
        APIRenderModelViewSet (class): Tests to check API rendering to ensure data is present, includes `APIRenderViewSet` tests.
    """


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

            mocked_setup = mocked_view_set.get_queryset()    # should only add two calls, if exists and the return


            for mock_call in list(qs.mock_calls):    # mock_calls with args means setter was called

                if len(mock_call.args) > 0:

                    setter_not_called = False


        assert setter_not_called
        assert qs.call_count == 2



    def test_view_func_get_serializer_class_cache_result(self):
        """Viewset Test

        Ensure that the `get_serializer_class` function caches the result under
        attribute `<viewset>.serializer_class`
        """

        view_set = self.viewset()

        view_set.request = MockRequest(
            user = self.view_user,
            organization = self.organization,
            viewset = self.viewset
        )

        view_set.kwargs = self.kwargs

        view_set.action = 'list'

        view_set.detail = False

        assert view_set.serializer_class is None    # Must be empty before init

        q = view_set.get_serializer_class()

        assert view_set.serializer_class is not None    # Must not be empty after init

        assert q == view_set.serializer_class


    def test_view_func_get_serializer_class_cache_result_used(self):
        """Viewset Test

        Ensure that the `get_serializer_class` function caches the result under
        attribute `<viewset>.serializer_class`
        """

        view_set = self.viewset()

        view_set.request = MockRequest(
            user = self.view_user,
            organization = self.organization,
            viewset = self.viewset
        )

        view_set.kwargs = self.kwargs
        view_set.action = 'list'
        view_set.detail = False

        mock_return = view_set.get_serializer_class()    # Real item to be used as mock return Some 
                                                         # functions use `Queryset` for additional filtering

        setter_not_called = True


        with patch.object(self.viewset, 'serializer_class', new_callable=PropertyMock) as qs:

            qs.return_value = mock_return

            mocked_view_set = self.viewset()

            mocked_view_set.kwargs = self.kwargs
            mocked_view_set.action = 'list'
            mocked_view_set.detail = False

            qs.reset_mock()    # Just in case

            mocked_setup = mocked_view_set.get_serializer_class()    # should only add two calls, if exists and the return


            for mock_call in list(qs.mock_calls):    # mock_calls with args means setter was called

                if len(mock_call.args) > 0:

                    setter_not_called = False


        assert setter_not_called
        assert qs.call_count == 2
