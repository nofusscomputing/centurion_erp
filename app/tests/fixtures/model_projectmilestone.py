import datetime
import pytest

from project_management.models.project_milestone import ProjectMilestone



@pytest.fixture( scope = 'class')
def model_projectmilestone():

    yield ProjectMilestone


@pytest.fixture( scope = 'class')
def kwargs_projectmilestone(django_db_blocker,
    kwargs_centurionmodel, kwargs_project, model_project
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        kwargs = kwargs_project.copy()
        kwargs.update({
            'name': 'pm' + random_str
        })

        project = model_project.objects.create(
            **kwargs
        )

    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    kwargs = {
        **kwargs,
        'name': 'pm_' + random_str,
        'project': project,
    }

    yield kwargs.copy()

    # with django_db_blocker.unblock():

    #     project.delete()    # milestone is cascade delete
