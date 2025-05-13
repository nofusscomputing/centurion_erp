import datetime
import django
import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from access.models.person import Person

from app.tests.unit.test_unit_models import (
    PyTestTenancyObjectInheritedCases,
)

from core.models.ticket_comment_base import TicketBase, TicketCommentBase, TicketCommentCategory

User = django.contrib.auth.get_user_model()



class TicketCommentBaseModelTestCases(
    PyTestTenancyObjectInheritedCases,
):

    base_model = TicketCommentBase

    sub_model_type = 'comment'
    """Sub Model Type
    
    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """

    kwargs_create_item: dict = {
        'parent': None,
        'ticket': '',
        'external_ref': 0,
        'external_system': TicketBase.Ticket_ExternalSystem.CUSTOM_1,
        'comment_type': sub_model_type,
        'category': '',
        'body': 'asdasdas',
        'private': False,
        'template': None,
        'source': TicketBase.TicketSource.HELPDESK,
        'user': '',
        'is_closed': True,
        'date_closed': '2025-05-08T17:10Z',
    }


    parameterized_fields: dict = {
        "is_global": {
            'field_type': None,
            'field_parameter_default_exists': None,
            'field_parameter_default_value': None,
            'field_parameter_verbose_name_type': None
        },
        "model_notes": {
            'field_type': None,
            'field_parameter_default_exists': None,
            'field_parameter_default_value': None,
            'field_parameter_verbose_name_type': None
        },
        "parent": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "ticket": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "external_ref": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "external_system": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "comment_type": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "category": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "body": {
            'field_type': models.fields.TextField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "private": {
            'field_type': models.fields.BooleanField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': False,
            'field_parameter_verbose_name_type': str,
        },
        "duration": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': 0,
            'field_parameter_verbose_name_type': str,
        },
        "estimation": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': 0,
            'field_parameter_verbose_name_type': str,
        },
        "template": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': True,
            'field_parameter_verbose_name_type': str,
        },
        "source": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': TicketBase.TicketSource.HELPDESK,
            'field_parameter_verbose_name_type': str,
        },
        "user": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_default_value': None,
            'field_parameter_verbose_name_type': str,
        },
        "is_closed": {
            'field_type': models.fields.BooleanField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': False,
            'field_parameter_verbose_name_type': str,
        },
        "date_closed": {
            'field_type': models.fields.DateTimeField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
    }


    @pytest.fixture( scope = 'class')
    def setup_model(self,
        request,
        model,
        django_db_blocker,
        organization_one,
        organization_two
    ):

        request.cls.model = model

        with django_db_blocker.unblock():

            random_str = datetime.datetime.now(tz=datetime.timezone.utc)

            request.cls.organization = organization_one

            request.cls.different_organization = organization_two

            kwargs_create_item = {}

            for base in reversed(request.cls.__mro__):

                if hasattr(base, 'kwargs_create_item'):

                    if base.kwargs_create_item is None:

                        continue

                    kwargs_create_item.update(**base.kwargs_create_item)


            if len(kwargs_create_item) > 0:

                request.cls.kwargs_create_item = kwargs_create_item


            request.cls.view_user = User.objects.create_user(username="ticket_comment_user_"+ str(random_str), password="password")

            comment_category = TicketCommentCategory.objects.create(
                organization = request.cls.organization,
                name = 'test cat comment'+ str(random_str)
            )

            ticket = TicketBase.objects.create(
                organization = request.cls.organization,
                title = 'tester comment ticket'+ str(random_str),
                description = 'aa',
                opened_by = request.cls.view_user,
            )

            user = Person.objects.create(
                organization = request.cls.organization,
                f_name = 'ip'+ str(random_str),
                l_name = 'funny'                
            )

            request.cls.kwargs_create_item.update({
                'category': comment_category,
                'ticket': ticket,
                'user': user,
            })


            if 'organization' not in request.cls.kwargs_create_item:

                request.cls.kwargs_create_item.update({
                    'organization': request.cls.organization
                })

        yield

        with django_db_blocker.unblock():

            del request.cls.kwargs_create_item

            comment_category.delete()

            for comment in ticket.ticketcommentbase_set.all():

                comment.delete()

            ticket.delete()

            user.delete()

            request.cls.view_user.delete()



    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_model,
        create_model,
    ):

        pass



    @pytest.fixture
    def ticket(self, request, django_db_blocker):

        with django_db_blocker.unblock():

            ticket = TicketBase.objects.create(
                organization = request.cls.organization,
                title = 'per function_ticket',
                opened_by = request.cls.view_user,
            )

        yield ticket


        with django_db_blocker.unblock():

            for comment in ticket.ticketcommentbase_set.all():

                comment.delete()

            ticket.delete()


    def test_create_validation_exception_no_organization(self):
        """ Tenancy objects must have an organization

        This test case is an over-ride of a test with the same name. this test
        is not required as the organization is derived from the ticket.

        Must not be able to create an item without an organization
        """

        pass


    def test_class_inherits_ticketcommentbase(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, TicketCommentBase)


    def test_attribute_meta_exists_permissions(self):
        """Attribute Check

        Ensure attribute `Meta.permissions` exists
        """

        assert hasattr(self.model._meta, 'permissions')


    def test_attribute_meta_not_none_permissions(self):
        """Attribute Check

        Ensure attribute `Meta.permissions` does not have a value of none
        """

        assert self.model._meta.permissions is not None


    def test_attribute_meta_type_permissions(self):
        """Attribute Check

        Ensure attribute `Meta.permissions` value is of type list
        """

        assert type(self.model._meta.permissions) is list


    def test_attribute_value_permissions_has_import(self):
        """Attribute Check

        Ensure attribute `Meta.permissions` value contains permission
        `import`
        """

        permission_found = False

        for permission, description in self.model._meta.permissions:

            if permission == 'import_' + self.model._meta.model_name:

                permission_found = True
                break

        assert permission_found


    def test_attribute_value_permissions_has_triage(self):
        """Attribute Check

        Ensure attribute `Meta.permissions` value contains permission
        `triage`
        """

        permission_found = False

        for permission, description in self.model._meta.permissions:

            if permission == 'triage_' + self.model._meta.model_name:

                permission_found = True
                break

        assert permission_found


    def test_attribute_value_permissions_has_purge(self):
        """Attribute Check

        Ensure attribute `Meta.permissions` value contains permission
        `purge`
        """

        permission_found = False

        for permission, description in self.model._meta.permissions:

            if permission == 'purge_' + self.model._meta.model_name:

                permission_found = True
                break

        assert permission_found


    def test_attribute_meta_type_sub_model_type(self):
        """Attribute Check

        Ensure attribute `Meta.sub_model_type` value is of type str
        """

        assert type(self.model._meta.sub_model_type) is str


    def test_attribute_meta_value_sub_model_type(self):
        """Attribute Check

        Ensure attribute `Meta.sub_model_type` value is correct
        """

        assert self.model._meta.sub_model_type == self.sub_model_type


    def test_attribute_type_get_comment_type(self):
        """Attribute Check

        Ensure attribute `get_comment_type` value is correct
        """

        assert self.item.get_comment_type == self.item._meta.sub_model_type



    def test_function_get_related_model(self):
        """Function Check

        Confirm function `get_related_model` returns `None` for self
        """

        assert self.item.get_related_model() == None



    def test_function_get_related_field_name(self):
        """Function Check

        Confirm function `get_related_field_name` returns an empty string
        for self
        """

        assert self.item.get_related_field_name() == ''



    def test_function_get_url(self):
        """Function Check

        Confirm function `get_url` returns the correct url
        """

        if self.item.parent:

            expected_value = '/core/ticket/' + str(self.item.ticket.id) + '/' + self.sub_model_type + '/' + str(
                self.item.parent.id) + '/threads/' + str(self.item.id) 

        else:

            expected_value = '/core/ticket/' + str( self.item.ticket.id) + '/' + self.sub_model_type + '/' + str(self.item.id)

        assert self.item.get_url() == '/api/v2' + expected_value


    def test_function_parent_object(self):
        """Function Check

        Confirm function `parent_object` returns the ticket
        """

        assert self.item.parent_object == self.item.ticket


    def test_function_clean_validation_mismatch_comment_type_raises_exception(self):
        """Function Check

        Ensure function `clean` does validation
        """

        valid_data = self.kwargs_create_item.copy()

        valid_data['comment_type'] = 'Nope'

        with pytest.raises(ValidationError) as err:

            self.model.objects.create(
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

        del valid_data['external_system']
        del valid_data['external_ref']

        comment = model.objects.create(
            **valid_data
        )

        comment.delete()

        assert spy.assert_called_once


    def test_function_save_called_slash_command(self, model, mocker, ticket):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(self.model, 'slash_command')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        del valid_data['external_system']
        del valid_data['external_ref']

        item = model.objects.create(
            **valid_data
        )

        spy.assert_called_with(item, valid_data['body'])



class TicketCommentBaseModelInheritedCases(
    TicketCommentBaseModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model TicketCommentBase
    """

    kwargs_create_item: dict = {}

    model = None


    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """



class TicketCommentBaseModelPyTest(
    TicketCommentBaseModelTestCases,
):


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

        spy = mocker.spy(self.model, 'slash_command')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        del valid_data['external_system']
        del valid_data['external_ref']

        item = model.objects.create(
            **valid_data
        )

        spy.assert_called_with(item, valid_data['body'])
