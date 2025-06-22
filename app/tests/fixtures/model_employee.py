import datetime
import pytest

from human_resources.models.employee import Employee



@pytest.fixture( scope = 'class')
def model_employee():

    yield Employee


@pytest.fixture( scope = 'class')
def kwargs_employee( kwargs_contact ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '').replace('-', '')

    kwargs = {
        **kwargs_contact.copy(),
        'employee_number':  int(str(random_str)[( len(random_str) - 13 ):])
    }

    yield kwargs.copy()
