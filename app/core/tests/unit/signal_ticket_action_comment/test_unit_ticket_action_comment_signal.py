import pytest

from types import FunctionType

from django.apps import apps

from centurion.tests.unit_class import ClassTestCases


@pytest.mark.model_ticketcategory
class TickActionCommentSignalTestCases(
    ClassTestCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'create_action_comment': {
                'arg_names': [ 'ticket', 'text', 'user' ],
                'function': True,
                'type': FunctionType,
            },
            'get_action_user': {
                'arg_names': [ 'instance', ],
                'function': True,
                'type': FunctionType,
            },
            'filter_models': {
                'arg_names': [ 'instance', 'created' ],
                'function': True,
                'type': FunctionType,
            },
            'ticket': {
                'arg_names': [ 'instance', ],
                'function': True,
                'type': FunctionType,
            },
            'ticket_m2m': {
                'arg_names': [ 'instance', 'field', 'model', 'action', 'ids' ],
                'function': True,
                'type': FunctionType,
            },
            'link_model_ticket': {
                'arg_names': [ 'instance', 'action' ],
                'function': True,
                'type': FunctionType,
            },
            'ticket_action_comment': {
                'arg_names': [ 'sender', 'instance', 'created', 'kwargs' ],
                'function': True,
                'type': FunctionType,
            },
        }


    @pytest.fixture( scope = 'class')
    def test_class(cls):

        from core import signal

        yield signal.ticket_action_comment



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_create_action_comment_calls_create(self, mocker,
        test_class, model_ticketbase, kwargs_ticketbase,
    ):
        """Test Function

        Ensure that method does call create for the action comment.
        """

        ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        create = mocker.patch('core.models.ticket_comment_action.TicketCommentAction.objects.create')

        test_class.create_action_comment(
            ticket = ticket,
            text = 'an action comment',
            user = ticket.opened_by
        )

        create.assert_called_once() 



    @pytest.mark.signal_action_comment
    def test_function_get_action_user_returns_user(self,
        test_class, model_centurionuser, kwargs_centurionuser
    ):
        """Test Function

        Ensure that if instance has a user field a user is returned.
        """

        user = model_centurionuser.objects.create( **kwargs_centurionuser() )

        class MockInstance:

            context = {
                'logger': None,
                'mockinstance': user
            }


        value = test_class.get_action_user(
            instance = MockInstance()
        )

        assert value == user



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_get_action_user_not_system(self,
        test_class, model_centurionuser, kwargs_centurionuser,
    ):
        """Test Function

        Ensure that if instance has a user field and the user is the system
        user, that none is returned.
        """

        user = model_centurionuser.objects.filter( username = 'system' )

        if len(user) != 1:
            
            kwargs = kwargs_centurionuser()
            kwargs['username'] = 'system'

            user = model_centurionuser.objects.create( **kwargs )
        else:
            user = user[0]



        class MockInstance:

            context = {
                'logger': None,
                'mockinstance': user
            }


        value = test_class.get_action_user(
            instance = MockInstance()
        )

        assert value == None



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_filter_models_not_centurion_user(self,
        test_class
    ):
        """Test Function

        Ensure that function filter_models is called for a non-centurionuser
        that it returns `None`.
        """

        class MockUser:

            username = 'system'        


        class MockInstance:
            context = {
                'logger': None,
                'mockinstance': MockUser()
            }


        value = test_class.get_action_user(
            instance = MockInstance()
        )

        assert value == None



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_filter_models_not_created_returns_ticket(self, mocker,
        test_class, model_ticketbase, kwargs_ticketbase,
        model_centurionuser, kwargs_centurionuser,
    ):
        """Test Function

        Ensure that when the instance is a ticket for function filter_models
        that the return is 'ticket' if it was not a creation event.
        """

        instance = model_ticketbase.objects.create( **kwargs_ticketbase() )

        user = model_centurionuser.objects.create( **kwargs_centurionuser() )

        create = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            'mockinstance': user
        })

        instance = model_ticketbase.objects.get(id = instance.id )

        instance.description = f'{instance.description}\n\nan edit'

        value = test_class.filter_models(
            instance = instance,
            created = False
        )

        assert value == 'ticket'



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_filter_models_created_returns_none(self, mocker,
        test_class, model_ticketbase, kwargs_ticketbase,
        model_centurionuser, kwargs_centurionuser,
    ):
        """Test Function

        Ensure that when the instance is a ticket for function filter_models
        that the return is None if it was a creation event.
        """

        instance = model_ticketbase.objects.create( **kwargs_ticketbase() )

        user = model_centurionuser.objects.create( **kwargs_centurionuser() )

        create = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            'mockinstance': user
        })

        value = test_class.filter_models(
            instance = instance,
            created = True
        )

        assert value == None



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_filter_models_no_user_returns_none(self, mocker,
        test_class, model_ticketbase, kwargs_ticketbase,
    ):
        """Test Function

        Ensure that when the instance is a ticket for function filter_models
        that the return is None if it was a creation event.
        """

        instance = model_ticketbase.objects.create( **kwargs_ticketbase() )

        create = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            'mockinstance': None
        })

        value = test_class.filter_models(
            instance = instance,
            created = False
        )

        assert value == None



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_filter_models_unknown_model_retuns_none(self, mocker,
        test_class,
        model_tenant, kwargs_tenant,
        model_centurionuser, kwargs_centurionuser,
    ):
        """Test Function

        Ensure that when the instance is a unknown for function filter_models
        that the return is None if it was a creation event.
        """

        instance = model_tenant.objects.create( **kwargs_tenant() )

        user = model_centurionuser.objects.create( **kwargs_centurionuser() )

        create = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            'mockinstance': user
        })

        value = test_class.filter_models(
            instance = instance,
            created = True
        )

        assert value == None



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_filter_models_link_model_returns_model(self, mocker,
        test_class,
        model_tenant, kwargs_tenant,
        model_contenttype,
        model_centurionuser, kwargs_centurionuser,
        model_ticketbase, kwargs_ticketbase,
    ):
        """Test Function

        Ensure that when the instance is a link of a model that the function
        returns 'model'.
        """

        the_model = model_tenant.objects.create( **kwargs_tenant() )

        ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        ticket_model = apps.get_model(
            app_label = model_tenant._meta.app_label,
            model_name = f'{model_tenant._meta.model_name}ticket'
        )

        content = model_contenttype.objects.get(
            app_label = ticket_model._meta.app_label,
            model = ticket_model._meta.model_name
        )

        instance = ticket_model.objects.create(
            content_type = content,
            model = the_model,
            ticket = ticket,
        )

        user = model_centurionuser.objects.create( **kwargs_centurionuser() )

        create = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            'mockinstance': user
        })

        value = test_class.filter_models(
            instance = instance,
            created = True
        )

        assert value == 'model'



    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    def test_function_filter_models_link_model_not_linkable_returns_none(self, mocker,
        test_class,
        model_tenant, kwargs_tenant,
        model_contenttype,
        model_centurionuser, kwargs_centurionuser,
        model_ticketbase, kwargs_ticketbase,
    ):
        """Test Function

        Ensure that when the instance is a link of a model that the function
        returns None if the model is not ticket linkable.
        """

        the_model = model_tenant.objects.create( **kwargs_tenant() )

        ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        ticket_model = apps.get_model(
            app_label = model_tenant._meta.app_label,
            model_name = f'{model_tenant._meta.model_name}ticket'
        )

        content = model_contenttype.objects.get(
            app_label = ticket_model._meta.app_label,
            model = ticket_model._meta.model_name
        )

        instance = ticket_model.objects.create(
            content_type = content,
            model = the_model,
            ticket = ticket,
        )

        user = model_centurionuser.objects.create( **kwargs_centurionuser() )

        mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            'mockinstance': user
        })

        mocker.patch('core.mixins.centurion.Centurion._ticket_linkable', False)

        value = test_class.filter_models(
            instance = instance,
            created = True
        )

        assert value == None



    @pytest.mark.signal_action_comment
    def test_function_ticket_calls_create_action_comment(self, mocker,
        test_class,
        model_centurionuser, kwargs_centurionuser,
        model_ticketbase, kwargs_ticketbase,
    ):
        """Test Function

        Ensure that when function `ticket` is called, it calls
        `create_action_comment`.
        """

        instance = model_ticketbase.objects.create( **kwargs_ticketbase() )

        instance._before = instance.get_audit_values()

        instance.description = f'{instance.description}\n\nan edit'

        user = model_centurionuser.objects.create( **kwargs_centurionuser() )

        mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            instance._meta.model_name: user
        })

        mocked_create_action_comment = mocker.patch.object(test_class, 'create_action_comment')

        test_class.ticket(
            instance = instance,
        )

        mocked_create_action_comment.assert_called_once()



    @pytest.mark.signal_action_comment
    def test_function_link_model_ticket_calls_create_action_comment(self, mocker,
        test_class,
        model_tenant, kwargs_tenant,
        model_contenttype,
        model_employee, kwargs_employee,
        model_ticketbase, kwargs_ticketbase,
    ):
        """Test Function

        Ensure that when function `link_model_ticket` is called it calls
        function`create_action_comment`.
        """

        the_model = model_tenant.objects.create( **kwargs_tenant() )

        ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        ticket_model = apps.get_model(
            app_label = model_tenant._meta.app_label,
            model_name = f'{model_tenant._meta.model_name}ticket'
        )

        content = model_contenttype.objects.get(
            app_label = ticket_model._meta.app_label,
            model = ticket_model._meta.model_name
        )

        instance = ticket_model.objects.create(
            content_type = content,
            model = the_model,
            ticket = ticket,
        )

        employee = model_employee.objects.create( **kwargs_employee() )

        mocked_create_action_comment = mocker.patch.object(test_class, 'get_action_user', return_value = employee.user)

        mocked_create_action_comment = mocker.patch.object(test_class, 'create_action_comment')

        test_class.link_model_ticket(
            instance = instance,
            action = 'dont matter'
        )

        mocked_create_action_comment.assert_called_once()



class TickActionCommentSignalInheritedCases(
    TickActionCommentSignalTestCases,
):
    pass



@pytest.mark.module_core
class TickActionCommentSignalPyTest(
    TickActionCommentSignalTestCases,
):
    pass
