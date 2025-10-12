import datetime
import pytest

from django.db import models

from rest_framework.exceptions import ValidationError


from core.models.ticket_comment_base import TicketCommentBase, TicketBase
from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.tickets
@pytest.mark.model_ticketcommentbase
class TicketCommentBaseModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_base_model': {
                'type': models.base.ModelBase,
                'value': TicketCommentBase,
            },
            '_audit_enabled': {
                'value': False
            },
            '_notes_enabled': {
                'value': False
            },
            '_is_submodel': {
                'value': False
            },
            '_ticket_linkable': {
                'value': False,
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

        return {
            "model_notes": {
                'blank': models.fields.NOT_PROVIDED,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.NOT_PROVIDED,
                'null': models.fields.NOT_PROVIDED,
                'unique': models.fields.NOT_PROVIDED,
            },
            "parent": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "ticket": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
            "external_ref": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.IntegerField,
                'null': True,
                'unique': False,
            },
            "external_system": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.IntegerField,
                'null': True,
                'unique': False,
            },
            "comment_type": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.CharField,
                'null': False,
                'unique': False,
            },
            "category": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "body": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.TextField,
                'null': True,
                'unique': False,
            },
            "private": {
                'blank': False,
                'default': False,
                'field_type': models.fields.BooleanField,
                'null': False,
                'unique': False,
            },
            "duration": {
                'blank': False,
                'default': 0,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
            "estimation": {
                'blank': False,
                'default': 0,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
            "template": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "source": {
                'blank': False,
                'default': TicketBase.TicketSource.HELPDESK,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
            "user": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "is_closed": {
                'blank': False,
                'default': False,
                'field_type': models.fields.BooleanField,
                'null': False,
                'unique': False,
            },
            "date_closed": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.DateTimeField,
                'null': True,
                'unique': False,
            }
        }


    @pytest.fixture
    def ticket(self, request, django_db_blocker, model_ticketbase, kwargs_ticketbase):

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
        random_str = str(random_str).replace(
                ' ', '').replace(':', '').replace('+', '').replace('.', '')

        with django_db_blocker.unblock():

            kwargs = kwargs_ticketbase()

            del kwargs['external_system']
            del kwargs['external_ref']

            kwargs['title'] = 'fn_ticket_' + str(random_str)

            ticket = model_ticketbase.objects.create(
                **kwargs,
            )

        yield ticket


        with django_db_blocker.unblock():

            for comment in ticket.ticketcommentbase_set.all():

                comment.delete()

            ticket.delete()


    def test_method_value_not_default___str__(self, model, model_instance ):
        pytest.xfail( reason = 'model does not require this function' )


    def test_model_tag_defined(self, model):
        pytest.xfail( reason = 'model does not require this function' )


    def test_class_inherits_TicketCommentBase(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, TicketCommentBase)


    def test_create_validation_exception_no_organization(self):
        """ Tenancy objects must have an organization

        This test case is an over-ride of a test with the same name. this test
        is not required as the organization is derived from the ticket.

        Must not be able to create an item without an organization
        """

        pass


    def test_class_inherits_ticketcommentbase(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, TicketCommentBase)


    def test_attribute_meta_exists_permissions(self, model):
        """Attribute Check

        Ensure attribute `Meta.permissions` exists
        """

        assert hasattr(model._meta, 'permissions')


    def test_attribute_meta_not_none_permissions(self, model):
        """Attribute Check

        Ensure attribute `Meta.permissions` does not have a value of none
        """

        assert model._meta.permissions is not None


    def test_attribute_meta_type_permissions(self, model):
        """Attribute Check

        Ensure attribute `Meta.permissions` value is of type list
        """

        assert type(model._meta.permissions) is list


    def test_attribute_value_permissions_has_import(self, model):
        """Attribute Check

        Ensure attribute `Meta.permissions` value contains permission
        `import`
        """

        permission_found = False

        for permission, description in model._meta.permissions:

            if permission == 'import_' + model._meta.model_name:

                permission_found = True
                break

        assert permission_found


    def test_attribute_value_permissions_has_triage(self, model):
        """Attribute Check

        Ensure attribute `Meta.permissions` value contains permission
        `triage`
        """

        permission_found = False

        for permission, description in model._meta.permissions:

            if permission == 'triage_' + model._meta.model_name:

                permission_found = True
                break

        assert permission_found


    def test_attribute_value_permissions_has_purge(self, model):
        """Attribute Check

        Ensure attribute `Meta.permissions` value contains permission
        `purge`
        """

        permission_found = False

        for permission, description in model._meta.permissions:

            if permission == 'purge_' + model._meta.model_name:

                permission_found = True
                break

        assert permission_found


    def test_attribute_meta_type_sub_model_type(self, model):
        """Attribute Check

        Ensure attribute `Meta.sub_model_type` value is of type str
        """

        assert type(model._meta.sub_model_type) is str


    def test_attribute_meta_value_sub_model_type(self, model):
        """Attribute Check

        Ensure attribute `Meta.sub_model_type` value is correct
        """

        assert model._meta.sub_model_type == self.sub_model_type


    def test_attribute_type_get_comment_type(self, model_instance):
        """Attribute Check

        Ensure attribute `get_comment_type` value is correct
        """

        assert model_instance.get_comment_type == model_instance._meta.sub_model_type



    def test_function_get_related_model(self, model_instance):
        """Function Check

        Confirm function `get_related_model` returns `None` for self
        """

        assert model_instance.get_related_model() == None


    def test_function_get_url(self, model_instance):
        """Function Check

        Confirm function `get_url` returns the correct url
        """

        if model_instance.parent:

            expected_value = '/core/ticket/' + str(
                model_instance.ticket.id) + '/' + self.sub_model_type + '/' + str(
                    model_instance.parent.id) + '/threads/' + str(model_instance.id)

        else:

            expected_value = '/core/ticket/' + str( 
                model_instance.ticket.id) + '/' + self.sub_model_type + '/' + str(
                    model_instance.id)

        assert model_instance.get_url(relative = True) == '/api/v2' + expected_value




    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        kwargs = {
            'ticket_id': model_instance.ticket.id,
            'pk': model_instance.id,
        }

        if model_instance._is_submodel:
            kwargs.update({
                'ticket_comment_model': model_instance._meta.sub_model_type
            })

        assert model_instance.get_url_kwargs() == kwargs



    def test_function_parent_object(self, model_instance):
        """Function Check

        Confirm function `parent_object` returns the ticket
        """

        assert model_instance.parent_object == model_instance.ticket


    def test_function_clean_validation_mismatch_comment_type_raises_exception(self, model):
        """Function Check

        Ensure function `clean` does validation
        """

        valid_data = self.kwargs_create_item.copy()

        valid_data['comment_type'] = 'Nope'

        with pytest.raises(ValidationError) as err:

            model.objects.create(
                **valid_data
            )

        assert err.value.get_codes()['comment_type'] == 'comment_type_wrong_endpoint'



    def test_function_called_clean_ticketcommentbase(self, model, mocker, ticket):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(TicketCommentBase, 'clean')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        comment = model.objects.create(
            **valid_data
        )

        comment.delete()

        assert spy.assert_called_once


    def test_function_save_called_slash_command(self, model, mocker, ticket):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(model, 'slash_command')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        item = model.objects.create(
            **valid_data
        )

        spy.assert_called_with(item, valid_data['body'])



    def test_method_delete_prevent_when_threads(self, mocker,
        model, model_ticketcommentbase, kwargs_ticketcommentbase, model_kwargs,
    ):

        mocker.patch(
            'core.models.centurion.CenturionModel.delete', return_value = None
        )

        kwargs = model_kwargs()
        del kwargs['external_ref']
        del kwargs['external_system']

        kwargs['ticket'].is_closed = False
        kwargs['ticket'].date_closed = None
        kwargs['ticket'].is_solved = False
        kwargs['ticket'].date_solved = None
        kwargs['ticket'].status = kwargs['ticket'].TicketStatus.NEW
        kwargs['ticket'].save()

        ticket = kwargs['ticket']

        parent_obj = model.objects.create( **kwargs )

        kwargs = kwargs_ticketcommentbase()
        del kwargs['external_ref']
        del kwargs['external_system']
        kwargs['parent'] = parent_obj
        kwargs['ticket'] = ticket

        model_ticketcommentbase.objects.create( **kwargs )
        model_ticketcommentbase.objects.create( **kwargs )
        model_ticketcommentbase.objects.create( **kwargs )
        model_ticketcommentbase.objects.create( **kwargs )

        assert len(parent_obj.threads.all()) > 0, 'Test requires there be threads.'

        with pytest.raises(models.ProtectedError):

            parent_obj.delete()



class TicketCommentBaseModelInheritedCases(
    TicketCommentBaseModelTestCases,
):

    sub_model_type = None

    def test_method_delete_calls_super_keep_parent_matches_is_sub_model(self, mocker, model_instance):
        """Test Class Method
        
        Ensure when method `delete` calls `super().delete` attribute
        `keep_parents` is `False` so that entire chain is deleted
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        mocker.patch(
            'django.db.models.query.QuerySet.get', return_value = model_instance
        )

        super_delete = mocker.patch(
            'django.db.models.base.Model.delete', return_value = None
        )

        mocker.patch(
            'core.mixins.centurion.Centurion.get_audit_values',
            return_value = {'key': 'value'}
        )

        model_instance.delete()


        super_delete.assert_called_with(using = None, keep_parents = False)




@pytest.mark.module_core
class TicketCommentBaseModelPyTest(
    TicketCommentBaseModelTestCases,
):

    sub_model_type = 'comment'



    # def test_function_clean_validation_close_raises_exception(self, ticket):
    #     """Function Check

    #     Ensure function `clean` does validation
    #     """

    #     valid_data = self.kwargs_create_item.copy()

    #     valid_data['ticket'] = ticket

    #     valid_data['external_ref'] = 9842

    #     del valid_data['date_closed']

    #     with pytest.raises(ValidationError) as err:

    #         self.model.objects.create(
    #             **valid_data
    #         )

    #     assert err.value.get_codes()['date_closed'] == 'ticket_closed_no_date'


    def test_function_save_called_slash_command(self, model, mocker, ticket):
        """Function Check

        This test case is a duplicate of a test with the same name. This
        test is required so that the base class `save()` function can be tested.

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(model, 'slash_command')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        item = model.objects.create(
            **valid_data
        )

        spy.assert_called_with(item, valid_data['body'])

    def test_function_get_url(self, model_instance):
        """Function Check

        Confirm function `get_url` returns the correct url
        """

        if model_instance.parent:

            expected_value = '/core/ticket/' + str(
                model_instance.ticket.id) + '/comment/' + str(
                    model_instance.parent.id) + '/threads/' + str(model_instance.id)

        else:

            expected_value = '/core/ticket/' + str( 
                model_instance.ticket.id) + '/comment/' + str(
                    model_instance.id)

        assert model_instance.get_url(relative = True) == '/api/v2' + expected_value
