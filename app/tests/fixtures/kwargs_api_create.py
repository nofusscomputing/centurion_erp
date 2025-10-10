import pytest

from django.db import models


@pytest.fixture(scope = 'class')
def kwargs_api_create(django_db_blocker, model_kwargs):


    kwargs: dict = {}

    with django_db_blocker.unblock():

        for field, value in model_kwargs().items():

            if value is None:
                continue

            if isinstance(value, models.Model):
                value = value.id

            elif isinstance(value, list):

                value_list = []

                for list_value in value:

                    if isinstance(list_value, models.Model):

                        value_list += [ list_value.id ]

                    else:

                        value_list += [ list_value ]

                value = value_list

            kwargs.update({
                field: value
            })

    yield kwargs

    del kwargs
