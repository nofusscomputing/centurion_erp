import datetime
import pytest

from project_management.models.project_types import ProjectType



@pytest.fixture( scope = 'class')
def model_projecttype():

    yield ProjectType


@pytest.fixture( scope = 'class')
def kwargs_projecttype(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'projecttype_' + random_str,
    }

    yield kwargs.copy()
