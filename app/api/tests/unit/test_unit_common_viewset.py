import django
import logging
import pytest
import random

from django.contrib.auth.models import ContentType, Permission

from rest_framework import viewsets

from api.permissions.default import DefaultDenyPermission
from access.models.tenant import Tenant as Organization, Tenant
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.react_ui_metadata import ReactUIMetadata
from api.viewsets.common.common import (
    Create,
    Destroy,
    List,
    Retrieve,
    Update,

    ModelViewSetBase,
    # StaticPageNumbering,

    CommonViewSet,
    CommonModelViewSet,
    CommonSubModelViewSet_ReWrite,

    CommonModelCreateViewSet,
    CommonModelListRetrieveDeleteViewSet,
    CommonModelRetrieveUpdateViewSet,
    CommonReadOnlyModelViewSet,
    CommonReadOnlyListModelViewSet,
    # CommonAuthUserReadOnlyModelViewSet,
    # CommonIndexViewset,
    # CommonPublicReadOnlyViewSet,
)

from centurion.tests.unit_class import ClassTestCases

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



@pytest.mark.api
@pytest.mark.viewset
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




class CommonCreatePyTest(
    CreateCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Create



@pytest.mark.api
@pytest.mark.viewset
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



class CommonDestroyPyTest(
    DestroyCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Destroy



@pytest.mark.api
@pytest.mark.viewset
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



class CommonListPyTest(
    ListCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return List



@pytest.mark.api
@pytest.mark.viewset
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



class CommonRetrievePyTest(
    RetrieveCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Retrieve



@pytest.mark.api
@pytest.mark.viewset
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



class CommonUpdatePyTest(
    UpdateCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return Update




@pytest.mark.api
@pytest.mark.viewset
class CommonViewSetTestCases(
    ClassTestCases,
):
    """Test Suite for class CommonViewSet"""

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        model_user, kwargs_user, organization_one
    ):

        with django_db_blocker.unblock():

            kwargs = kwargs_user()
            kwargs['username'] = "test_user1-" + str(
                str(
                    random.randint(1,99))
                    + str(random.randint(300,399))
                    + str(random.randint(400,499)
                )
            ),

            user = model_user.objects.create( **kwargs )

        view_set = viewset()
        model = getattr(view_set, 'model', None)

        if not model:
            model = Tenant

        request = MockRequest(
            user = user,
            model = model,
            viewset = viewset,
            organization = organization_one
        )

        view_set.request = request
        view_set.kwargs = {}

        yield view_set

        del view_set.request

        with django_db_blocker.unblock():

            user.delete()


    @pytest.fixture( scope = 'function')
    def test_class(cls, viewset_mock_request):

        yield viewset_mock_request



    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': logging.Logger,
                'value': None
            },
            '_model_documentation': {
                'type': str,
                'value': None
            },
            '_permission_required': {
                'type': type(None),
                'value': None
            },
            '_queryset': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': str,
                'value': None
            },
            'documentation': {
                'type': str,
                'value': None
            },
            'metadata_class': {
                'type': type,
                'value': ReactUIMetadata
            },
            'metadata_markdown': {
                'type': bool,
                'value': False
            },
            'model_documentation': {
                'type': str,
                'value': None
            },
            'page_layout': {
                'type': list,
                'value': []
            },
            'permission_classes': {
                'type': list,
                'value': [
                    DefaultDenyPermission,
                ]
            },
            'table_fields': {
                'type': list,
                'value': []
            },
            'view_description': {
                'type': str,
                'value': None
            },
            'view_name': {
                'type': str,
                'value': None
            }
        }



    def test_class_inherits_viewsets_viewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.ViewSet`
        """

        assert issubclass(viewset, viewsets.ViewSet)


    def test_view_func_get_queryset_cache_result(self, mocker, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request
        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as queries:

            assert view_set._queryset is None    # Must be empty before init

            q = view_set.get_queryset()

            evaluate = len(view_set.get_queryset())

            initial_db_queries = len(queries)

            assert view_set._queryset is not None    # Must not be empty after init

            assert len(queries) == initial_db_queries


    def test_view_func_get_queryset_cache_result_used(self, mocker, viewset, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request
        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        qs = mocker.spy(view_set.model, 'objects')

        view_set.get_queryset()    # Initial QuerySet fetch/filter and cache

        initial_method_calls = len(qs.method_calls)
        initial_mock_calls = len(qs.mock_calls)

        assert initial_method_calls > 0       # one call to .all()
        assert initial_mock_calls > 0         # calls = .user( ...), .user().all(), .user().all().filter()

        view_set.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == initial_method_calls
        assert len(qs.mock_calls) == initial_mock_calls

    # ToDo: get_back_url

    # ToDo: get_model_documentation

    # ToDo: get_page_layout

    # ToDo: get_return_url

    # ToDo: get_table_fields

    # ToDo: get_view_description

    # ToDo: get_view_name



class CommonViewSetPyTest(
    CommonViewSetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            }
        }


    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )


@pytest.mark.api
@pytest.mark.viewset
class CommonViewSetAPIRenderOptionsCases:    # ToDo
    """Test Cases for ViewSets that inherit from CommonViewSet
    
    Dont Include this test suite directy, use the test cases below `*InheritedTest`
    """

    http_options_response_list = None
    """Inherited class must make and store here a HTTP/Options request"""


    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_allowed_methods_exists(self):
        """Attribute Test

        Attribute `allowed_methods` must exist
        """

        assert 'allowed_methods' in self.http_options_response_list.data


    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_allowed_methods_not_empty(self):
        """Attribute Test

        Attribute `allowed_methods` must return a value
        """

        assert len(self.http_options_response_list.data['allowed_methods']) > 0


    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_allowed_methods_type(self):
        """Attribute Test

        Attribute `allowed_methods` must be of type list
        """

        assert type(self.http_options_response_list.data['allowed_methods']) is list


    @pytest.mark.skip(reason = 'see #895, tests being refactored')
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



    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_view_description_exists(self):
        """Attribute Test

        Attribute `description` must exist
        """

        assert 'description' in self.http_options_response_list.data


    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_view_description_not_empty(self):
        """Attribute Test

        Attribute `view_description` must return a value
        """

        assert self.http_options_response_list.data['description'] is not None


    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_view_description_type(self):
        """Attribute Test

        Attribute `view_description` must be of type str
        """

        assert type(self.http_options_response_list.data['description']) is str



    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_view_name_exists(self):
        """Attribute Test

        Attribute `view_name` must exist
        """

        assert 'name' in self.http_options_response_list.data


    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_view_name_not_empty(self):
        """Attribute Test

        Attribute `view_name` must return a value
        """

        assert self.http_options_response_list.data['name'] is not None


    @pytest.mark.skip(reason = 'see #895, tests being refactored')
    def test_api_render_field_view_name_type(self):
        """Attribute Test

        Attribute `view_name` must be of type str
        """

        assert type(self.http_options_response_list.data['name']) is str



@pytest.mark.api
@pytest.mark.viewset
class ModelViewSetBaseCases(
    CommonViewSetTestCases,
):
    """Test Suite for class ModelViewSetBase"""


    @property
    def parameterized_class_attributes(self):
        return {
            'filterset_fields': {
                'type': list,
                'value': []
            },
            'lookup_value_regex': {
                'type': str,
                'value': '[0-9]+'
            },
            'model': {
                'type': django.db.models.base.ModelBase,
                'value': None
            },
            'search_fields': {
                'type': list,
                'value': []
            },
            'serializer_class': {
                'type': str,
                'value': None
            },
            'view_serializer_name': {
                'type': str,
                'value': None
            },
        }


    def test_class_inherits_modelviewsetbase(self, viewset):
        """Class Inheritence check

        Class must inherit from `ModelViewSetBase`
        """

        assert issubclass(viewset, CommonViewSet)



class CommonModelViewSetBasePyTest(
    ModelViewSetBaseCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ModelViewSetBase


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }


    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



class ModelViewSetTestCases(
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



class CommonModelViewSetPyTest(
    ModelViewSetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonModelViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }


    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



class CommonSubModelViewSetTestCases(
    ModelViewSetTestCases
):


    @property
    def parameterized_class_attributes(self):
        return {
            'base_model': {
                'type': type,
                'value': None
            },
            'model_kwarg': {
                'type': str,
                'value': None
            },
            'model_suffix': {
                'type': str,
                'value': None
            }
        }


    def test_class_inherits_submodelviewsetbase(self, viewset):
        """Class Inheritence check

        Class must inherit from `SubModelViewSet`
        """

        assert issubclass(viewset, CommonSubModelViewSet_ReWrite)



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


    # ToDo: Test returned serializer for all CRUD. Add, Change, Delete, Replace and View



class CommonSubModelViewSetPyTest(
    CommonSubModelViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonSubModelViewSet_ReWrite


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'base_model': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': django.db.models.NOT_PROVIDED,
                'value': django.db.models.NOT_PROVIDED
            },
            'model_suffix': {
                'type': type(None),
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'model_kwarg': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }


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
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



class ModelCreateViewSetTestCases(
    ModelViewSetBaseCases,
    CreateCases,
):
    """Test Suite for class ModelCreateViewSet"""

    def test_class_inherits_viewsets_genericviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(viewset, viewsets.GenericViewSet)



class CommonModelCreateViewSetPyTest(
    ModelCreateViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonModelCreateViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }


    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



class ModelListRetrieveDeleteViewSetTestCases(
    ModelViewSetBaseCases,
    ListCases,
    RetrieveCases,
    DestroyCases,
):
    """Test Suite for class ModelListRetrieveDeleteViewSet"""


    def test_class_inherits_viewsets_genericviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(viewset, viewsets.GenericViewSet)



class CommonModelListRetrieveDeleteViewSetPyTest(
    ModelListRetrieveDeleteViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonModelListRetrieveDeleteViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }


    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



class ModelRetrieveUpdateViewSetTestCases(
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



class CommonModelRetrieveUpdateViewSetPyTest(
    ModelRetrieveUpdateViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonModelRetrieveUpdateViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }


    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



class ReadOnlyModelViewSetTestCases(
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



class CommonReadOnlyModelViewSetPyTest(
    ReadOnlyModelViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonReadOnlyModelViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }


    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



class ReadOnlyListModelViewSetTestCases(
    ModelViewSetBaseCases,
    ListCases,
):
    """Test Suite for class ReadOnlyListModelViewSet"""


    def test_class_inherits_viewsets_genericviewset(self, viewset):
        """Class Inheritence check

        Class must inherit from `viewsets.GenericViewSet`
        """

        assert issubclass(viewset, viewsets.GenericViewSet)



class CommonReadOnlyListModelViewSetPyTest(
    ReadOnlyListModelViewSetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return CommonReadOnlyListModelViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }



    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )



# class AuthUserReadOnlyModelViewSetTestCases(
#     ReadOnlyModelViewSetTestCases,
# ):
#     """Test Suite for class AuthUserReadOnlyModelViewSet"""


#     @property
#     def parameterized_class_attributes(self):
#         return {
#             'permission_classes': {
#                 'type': list,
#                 'value': [
#                     IsAuthenticated,
#                 ]
#             }
#         }



# class AuthUserReadOnlyModelViewSetPyTest(
#     AuthUserReadOnlyModelViewSetTestCases,
# ):


#     @pytest.fixture( scope = 'function' )
#     def viewset(self):
#         return AuthUserReadOnlyModelViewSet



#     def test_view_func_get_queryset_cache_result(self):
#         pytest.xfail( reason = 'base class is abstract with no model' )

#     def test_view_func_get_queryset_cache_result_used(self):
#         pytest.xfail( reason = 'base class is abstract with no model' )



# class IndexViewsetCases(
#     ModelViewSetBaseCases,
# ):
#     """Test Suite for class IndexViewset"""


#     @property
#     def parameterized_class_attributes(self):
#         return {
#             'permission_classes': {
#                 'type': list,
#                 'value': [
#                     IsAuthenticated,
#                 ]
#             }
#         }



# class IndexViewsetPyTest(
#     IndexViewsetCases,
# ):


#     @pytest.fixture( scope = 'function' )
#     def viewset(self):
#         return IndexViewset


#     @property
#     def parameterized_class_attributes(self):
#         return {
#             '_log': {
#                 'type': type(None),
#                 'value': None
#             },
#             '_model_documentation': {
#                 'type': type(None),
#                 'value': None
#             },
#             'back_url': {
#                 'type': type(None),
#                 'value': None
#             },
#             'documentation': {
#                 'type': type(None),
#                 'value': None
#             },
#             'model': {
#                 'type': type(None),
#                 'value': None
#             },
#             'model_documentation': {
#                 'type': type(None),
#                 'value': None
#             },
#             'serializer_class': {
#                 'type': type(None),
#                 'value': None
#             },
#             'view_description': {
#                 'type': type(None),
#                 'value': None
#             },
#             'view_name': {
#                 'type': type(None),
#                 'value': None
#             },
#             'view_serializer_name': {
#                 'type': type(None),
#                 'value': None
#             }
#         }


#     def test_view_func_get_queryset_cache_result(self):
#         pytest.xfail( reason = 'base class is abstract with no model' )

#     def test_view_func_get_queryset_cache_result_used(self):
#         pytest.xfail( reason = 'base class is abstract with no model' )



# class PublicReadOnlyViewSetTestCases(
#     ReadOnlyListModelViewSetTestCases,
# ):
#     """Test Suite for class PublicReadOnlyViewSet"""




# class PublicReadOnlyViewSetPyTest(
#     PublicReadOnlyViewSetTestCases,
# ):


#     @pytest.fixture( scope = 'function' )
#     def viewset(self):
#         return PublicReadOnlyViewSet




#########################################################################################
#
#    Use the below test cases for Viewset that inherit the class `(.+)InheritedCases`
#
#########################################################################################



# class AuthUserReadOnlyModelViewSetInheritedCases(
#     AuthUserReadOnlyModelViewSetTestCases,
# ):

#     pass



# class IndexViewsetInheritedCases(
#     IndexViewsetCases,
# ):


#     def test_view_func_get_queryset_cache_result(self):
#         pytest.xfail( reason = 'base class is abstract with no model' )

#     def test_view_func_get_queryset_cache_result_used(self):
#         pytest.xfail( reason = 'base class is abstract with no model' )



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
    CommonViewSetAPIRenderOptionsCases,
):
    """Test Suite for classes that inherit ModelViewSet
    
    Use this Test Suite for ViewSet classes that inherit from ModelViewSet
    """


    @property
    def parameterized_class_attributes(self):
        return {
            # '_log': {
            #     'type': logging.Logger,
            #     'value': None
            # },
            '_log': {
                'type': type(None),
            },
        }




class CommonSubModelViewSetInheritedCases(
    CommonSubModelViewSetTestCases,
    CommonViewSetAPIRenderOptionsCases,
):
    """Test Suite for classes that inherit SubModelViewSet
    
    Use this Test Suite for ViewSet classes that inherit from SubModelViewSet
    """


    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        model_user, kwargs_user, organization_one, model
    ):

        with django_db_blocker.unblock():

            kwargs = kwargs_user()
            kwargs['username'] = "test_user1-" + str(
                str(
                    random.randint(1,99))
                    + str(random.randint(300,399))
                    + str(random.randint(400,499)
                )
            ),

            user = model_user.objects.create( **kwargs )

        view_set = viewset()

        request = MockRequest(
            user = user,
            model = model,
            viewset = viewset,
            organization = organization_one,
        )

        view_set.request = request
        view_set.kwargs = {
            view_set.model_kwarg: model._meta.model_name
        }

        yield view_set

        del view_set.request

        with django_db_blocker.unblock():

            user.delete()


    @property
    def parameterized_class_attributes(self):
        return {
            # '_log': {
            #     'type': logging.Logger,
            #     'value': None
            # },
            '_log': {
                'type': type(None),
            },
            'model_suffix': {
                'type': str,
                'value': None
            },
            'base_model': {
                'type': django.db.models.base.ModelBase,
                'value': None
            },
            'model_kwarg': {
                'type': str,
                'value': None
            }
        }


    # ToDo: model

    # ToDo: related_objects

    # ToDo: get_serializer_class

    # ToDo: related_objects



# class PublicReadOnlyViewSetInheritedCases(
#     PublicReadOnlyViewSetTestCases,
# ):

#     pass



class CommonReadOnlyListModelViewSetInheritedCases(
    ReadOnlyListModelViewSetTestCases,
):
    pass

class CommonReadOnlyModelViewSetInheritedCases(
    ReadOnlyModelViewSetTestCases,
):

    pass
