import datetime
import pytest

from project_management.models.project_states import ProjectState



@pytest.fixture( scope = 'class')
def model_projectstate():

    yield ProjectState


@pytest.fixture( scope = 'class')
def kwargs_projectstate(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    kwargs = {
        **kwargs,
        'name': 'projectstate_' + random_str,
    }

    yield kwargs.copy()
