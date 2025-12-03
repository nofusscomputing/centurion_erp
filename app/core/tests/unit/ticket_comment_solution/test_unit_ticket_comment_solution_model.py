import pytest

from django.apps import apps
from django.db import models

from access.tests.unit.managers.test_unit_tenancy_manager import has_arg_kwarg

from core.models.ticket_comment_solution import TicketCommentSolution

from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_model import (
    TicketCommentBaseModelInheritedCases
)



@pytest.mark.model_ticketcommentsolution
class TicketCommentSolutionModelTestCases(
    TicketCommentBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'value': False
            },
            '_is_submodel': {
                'value': True
            },
            '_notes_enabled': {
                'value': False
            },
            'model_tag': {
                'type': type(None),
                'value': None
            },
            'url_model_name': {
                'type': str,
                'value': 'ticket_comment_base'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {}

    @pytest.fixture( scope = 'function', autouse = True)
    def model_instance(cls, model_kwarg_data, model, model_kwargs):

        class MockModel(model):
            class Meta:
                app_label = 'core'
                verbose_name = 'mock instance'
                managed = False

        if 'mockmodel' in apps.all_models['core']:

            del apps.all_models['core']['mockmodel']

        if model._meta.abstract:

            instance = MockModel()

        else:

            kwargs = model_kwargs()

            kwargs['ticket'].is_closed = False
            kwargs['ticket'].date_closed = None
            kwargs['ticket'].is_solved = False
            kwargs['ticket'].date_solved = None

            kwargs['ticket'].status = kwargs['ticket'].TicketStatus.NEW

            kwargs['ticket'].save()

            instance = model_kwarg_data(
                model = model,
                model_kwargs = kwargs,
                create_instance = True,
            )

            instance = instance['instance']


        yield instance

        if 'mockmodel' in apps.all_models['core']:

            del apps.all_models['core']['mockmodel']

        if type(instance) is dict:

            instance['instance'].delete()

        elif instance.id and type(instance) is not MockModel:

            instance.delete()

        del instance



    def test_method_centurion_save_called(self, mocker, model_instance):
        """Test Class Method

        Ensure method `core.mixins.centurion.Centurion.save()` is called
        when `model.save()` is called.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        save = mocker.patch('core.mixins.centurion.Centurion.save', return_value = None)


        model_instance.save()

        save.assert_called()


    def test_class_inherits_ticketcommentsolution(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, TicketCommentSolution)



    def test_function_called_clean_ticketcommentsolution(self, model, mocker, model_kwargs, ticket):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(TicketCommentSolution, 'clean')

        valid_data = model_kwargs()

        valid_data['ticket'] = ticket

        # del valid_data['external_system']
        # del valid_data['external_ref']

        comment = model.objects.create(
            **valid_data
        )

        comment.delete()

        assert spy.assert_called_once



class TicketCommentSolutionModelInheritedCases(
    TicketCommentSolutionModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_core
class TicketCommentSolutionModelPyTest(
    TicketCommentSolutionModelTestCases,
):

    sub_model_type = 'solution'


    @pytest.mark.regression
    def test_method_clean_called(self, mocker, model, model_instance):
        """Test Method

        Ensure method `clean` is called once only.
        """

        clean = mocker.spy(model_instance, 'clean')

        model_instance.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        model_instance.ticket.is_solved = False

        model_instance.save()

        clean.assert_called_once()



    @pytest.mark.regression
    def test_method_clean_fields_called(self, mocker, model, model_instance):
        """Test Method

        Ensure method `clean_fields` is called once only.
        """

        clean_fields = mocker.spy(model_instance, 'clean_fields')

        model_instance.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        model_instance.ticket.is_solved = False

        model_instance.save()

        clean_fields.assert_called_once()



    @pytest.mark.regression
    def test_method_full_clean_called(self, mocker, model, model_instance):
        """Test Method

        Ensure method `full_clean` is called once only.
        """

        full_clean = mocker.spy(model_instance, 'full_clean')

        model_instance.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        model_instance.ticket.is_solved = False

        model_instance.save()

        full_clean.assert_called_once()



    @pytest.mark.regression
    def test_method_validate_constraints_called(self, mocker, model, model_instance):
        """Test Method

        Ensure method `validate_constraints` is called once only.
        """

        validate_constraints = mocker.spy(model_instance, 'validate_constraints')

        model_instance.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        model_instance.ticket.is_solved = False

        model_instance.save()

        validate_constraints.assert_called_once()



    @pytest.mark.regression
    def test_method_validate_unique_called(self, mocker, model, model_instance):
        """Test Method

        Ensure method `validate_unique` is called once only.
        """

        validate_unique = mocker.spy(model_instance, 'validate_unique')

        model_instance.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        model_instance.ticket.is_solved = False

        model_instance.save()

        validate_unique.assert_called_once()


    def test_manager_tenancy_filter_tenant(self, mocker,
        model_instance, model, api_request_permissions
    ):

        filter = mocker.spy(models.QuerySet, 'filter')

        obj = model_instance

        obj.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        obj.ticket.is_solved = False

        obj.ticket.save()

        if hasattr(model, 'organization'):
            obj.organization = api_request_permissions['tenancy']['user']
            obj.save()

        filter.reset_mock()

        model.objects.user(
            user = api_request_permissions['user']['view'],
            permission = [ str( model._meta.app_label + '.view_' + model._meta.model_name ) ]
        ).all()

        assert any(
            has_arg_kwarg(call = c, key = 'organization__in') 
            and c.args[0].model is model for c in filter.call_args_list
        )


    def test_method_clean_calls_super_centurion_mixin(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        super_clean = mocker.patch('django.db.models.base.Model.clean', return_value = None)

        model_instance.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        model_instance.ticket.is_solved = False

        model_instance.ticket.save()

        super_clean.reset_mock()

        model_instance.clean()


        super_clean.assert_called_once()


    def test_method_clean_calls_super_centurion_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        super_clean = mocker.patch(
            'core.models.centurion.CenturionModel.clean', return_value = None
        )

        model_instance.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        model_instance.ticket.is_solved = False

        model_instance.ticket.save()

        super_clean.reset_mock()

        model_instance.clean()

        super_clean.assert_called_once()


    def test_method_clean_calls_super_tenancy_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        super_clean = mocker.patch('django.db.models.base.Model.clean', return_value = None)

        model_instance.ticket.status = model_instance.ticket.__class__.TicketStatus.NEW
        model_instance.ticket.is_solved = False

        model_instance.ticket.save()

        super_clean.reset_mock()

        model_instance.clean()


        super_clean.assert_called_once()
