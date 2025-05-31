import pytest

from django.db import models


@pytest.fixture(scope = 'class')
def kwargs_api_create(django_db_blocker, model_kwargs):


    kwargs: dict = {}

    with django_db_blocker.unblock():

        for field, value in model_kwargs.items():

            if value is None:
                continue

            if isinstance(value, models.Model):
                value = value.id

            kwargs.update({
                field: value
            })

    yield kwargs

    del kwargs
