import datetime
import pytest

from project_management.models.projects import Project



@pytest.fixture( scope = 'class')
def model_project():

    yield Project


@pytest.fixture( scope = 'class')
def kwargs_project(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'project_' + random_str,
        'priority': Project.Priority.LOW,
    }

    yield kwargs.copy()
