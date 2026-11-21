import pytest

from django.db import models
from types import NoneType

from access.permissions.super_user import SuperUserPermissions

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.permissions.ticket import TicketPermission
from core.viewsets.ticket_comment import (
    TicketBase,
    TicketCommentBase,
    ViewSet
)



@pytest.mark.tickets
@pytest.mark.model_ticketcommentbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_has_import': {
                'type': bool,
                'value': False
            },
            '_has_purge': {
                'type': bool,
                'value': False
            },
            '_has_triage': {
                'type': bool,
                'value': False
            },
            '_model_documentation': {
                'type': NoneType,
            },
            'base_model': {
                'value': TicketCommentBase,
            },
            'back_url': {
                'type': NoneType,
            },
            'documentation': {
                'type': NoneType,
            },
            'filterset_fields': {
                'value': [
                    'category',
                    'external_system',
                    'external_system',
                    'is_template',
                    'organization',
                    'parent',
                    'source',
                    'template',
                ]
            },
            'model': {
                'value': TicketCommentBase
            },
            'model_documentation': {
                'type': NoneType,
            },
            'model_kwarg': {
                'value':'model_name',
            },
            'model_suffix': {
                'type': NoneType,
            },
            'parent_model': {
                'type': models.base.ModelBase,
                'value': TicketBase
            },
            'parent_model_pk_kwarg': {
                'value': 'ticket_id'
            },
            'permission_classes': {
                'type': list,
                'value': [ TicketPermission | SuperUserPermissions ]
            },
            'perms_map': {
                'type': dict
            },
            'search_fields': {
                'value': [
                    'body',
                ]
            },
            'serializer_class': {
                'type': NoneType,
            },
            'view_description': {
                'value': 'Comments made on Ticket'
            },
            'view_name': {
                'type': NoneType,
            },
            'view_serializer_name': {
                'type': NoneType,
            },
        }

    def test_function_get_parent_model(self, mocker, viewset):
        """Test class function

        Ensure that when function `get_parent_model` is called it returns the value
        of `viewset.parent_model`.

        For all models that dont have attribute `viewset.parent_model` set, it should
        return None
        """

        assert viewset().get_parent_model() is TicketBase



class TicketCommentBaseViewsetInheritedCases(
    ViewsetTestCases,
):

    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires kwarg `model_name`' )
    def test_view_func_get_serializer_class_create(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct create
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'create'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_create_kwargs(self, viewset, model, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct create
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'create'

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires kwarg `model_name`' )
    def test_view_func_get_serializer_class_partial_update(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct partial_update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'partial_update'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_partial_update_kwargs(self, viewset, model, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct partial_update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'partial_update'

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires kwarg `model_name`' )
    def test_view_func_get_serializer_class_update(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'update'


        assert view_set.get_serializer_class() == model_serializer['model']



    def test_view_func_get_serializer_class_update_kwargs(self, viewset, model, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct update
        serializer for the model in question.
        """

        view_set = viewset()

        view_set.action = 'update'

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['model']



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'viewset requires kwarg `model_name`' )
    def test_view_func_get_serializer_class_view(self, viewset, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'


        assert view_set.get_serializer_class() == model_serializer['view']



    def test_view_func_get_serializer_class_view_kwargs(self, viewset, model, model_serializer):
        """ Function Test

        Function `get_serializer_class` must return the correct view serializer
        for the model in question
        """

        view_set = viewset()

        view_set.action = 'list'

        view_set.kwargs = {
            'model_name': model._meta.model_name
        }


        assert view_set.get_serializer_class() == model_serializer['view']




@pytest.mark.module_core
class TicketCommentBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
