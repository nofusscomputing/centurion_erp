import pytest

from types import FunctionType

from pytest_simplified.suites.attributes import ClassAttributesTestCases
from pytest_simplified.suites.functions import ClassFunctionsTestCases



@pytest.mark.model_ticketcategory
class TickActionCommentSignalTestCases(
    ClassAttributesTestCases,
    ClassFunctionsTestCases
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



class TickActionCommentSignalInheritedCases(
    TickActionCommentSignalTestCases,
):
    pass



@pytest.mark.module_core
class TickActionCommentSignalPyTest(
    TickActionCommentSignalTestCases,
):
    pass
