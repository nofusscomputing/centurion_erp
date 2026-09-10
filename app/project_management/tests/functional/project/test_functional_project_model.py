import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_project
class ProjectModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):

    duration_params = [
        # name, duration_slash_command, expected_seconds
        ('single_ticket_single_comment', [ '1h' ], 3600),
        ('single_ticket_multiple_comment', [ '30m', '30m' ], 3600),
        ('multiple_ticket_single_comment', [[ '30m' ], [ '30m' ]], 3600),
        ('multiple_ticket_multiple_comment', [[ '15m', '15m' ], [ '15m', '15m' ]], 3600),
    ]

    @pytest.mark.parametrize(
        argnames = ['name', 'duration_slash_command', 'expected_seconds'],
        argvalues = duration_params,
        ids = [ name for name, *other in duration_params ],
    )
    def test_field_duration(self, created_model,
        name, duration_slash_command, expected_seconds,
        model_projecttaskticket, kwargs_projecttaskticket,
        model_ticketcommentbase, kwargs_ticketcommentbase
    ):
        """Test field

        Ensure that field `duration_project` calculates the correct time
        """

        ticket_comment_kwargs = kwargs_ticketcommentbase()

        def task_factory():
            kwargs = kwargs_projecttaskticket()
            del kwargs['milestone']
            kwargs['project'] = created_model

            return model_projecttaskticket.objects.create( **kwargs )


        if isinstance(duration_slash_command[0], str ):

            task = task_factory()

            for comment in duration_slash_command:

                model_ticketcommentbase.objects.create(
                    ticket = task,
                    body = f"a comment\n/spend {comment}",
                    user = ticket_comment_kwargs['user']
                )

        elif isinstance(duration_slash_command[0], list):

            for ticket in duration_slash_command:

                task = task_factory()

                for comment in ticket:

                    model_ticketcommentbase.objects.create(
                        ticket = task,
                        body = f"a comment\n/spend {comment}",
                        user = ticket_comment_kwargs['user']
                    )


        assert created_model.duration_project == expected_seconds



    @pytest.mark.skip( reason = 'No slash command for estimation yet.' )
    @pytest.mark.parametrize(
        argnames = ['name', 'duration_slash_command', 'expected_seconds'],
        argvalues = duration_params,
        ids = [ name for name, *other in duration_params ],
    )
    def test_field_estimation(self, created_model,
        name, duration_slash_command, expected_seconds,
        model_projecttaskticket, kwargs_projecttaskticket,
        model_ticketcommentbase, kwargs_ticketcommentbase
    ):
        """Test field

        Ensure that field `estimation_project` calculates the correct time
        """

        ticket_comment_kwargs = kwargs_ticketcommentbase()

        def task_factory():
            kwargs = kwargs_projecttaskticket()
            del kwargs['milestone']
            kwargs['project'] = created_model

            return model_projecttaskticket.objects.create( **kwargs )


        if isinstance(duration_slash_command[0], str ):

            task = task_factory()

            for comment in duration_slash_command:

                model_ticketcommentbase.objects.create(
                    ticket = task,
                    body = f"a comment\n/estimate {comment}",
                    user = ticket_comment_kwargs['user']
                )

        elif isinstance(duration_slash_command[0], list):

            for ticket in duration_slash_command:

                task = task_factory()

                for comment in ticket:

                    model_ticketcommentbase.objects.create(
                        ticket = task,
                        body = f"a comment\n/spend {comment}",
                        user = ticket_comment_kwargs['user']
                    )


        assert created_model.estimation_project == 0




class ProjectModelInheritedCases(
    ProjectModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectModelPyTest(
    ProjectModelTestCases,
):
    pass
