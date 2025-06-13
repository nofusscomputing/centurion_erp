import datetime
import json
import pytest

from django.db import models


@pytest.fixture( scope = 'class' )
def model_kwarg_data():

    def data(model, model_kwargs, model_instance = None, create_instance = False) -> dict:

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
        random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '').replace('-', '')

        # data = {}


        kwargs = {}

        many_field = {}

        for field, value in model_kwargs.items():

            if not hasattr(getattr(model, field), 'field'):
                continue

            if isinstance(getattr(model, field).field, models.ManyToManyField):

                if field in many_field:

                    many_field[field] += [ value ]

                else:

                    many_field.update({
                        field: [
                            value
                        ]
                    })

                continue

            elif(
                getattr(model, field).field.unique
                and not isinstance(getattr(model, field).field, models.UUIDField)
                and not isinstance(getattr(model, field).field, models.ForeignKey)

            ):

                value = 'a' + random_str

            kwargs.update({
                field: value
            })

        instance = None

        if create_instance:

            instance =model.objects.create(
                **kwargs
            )


            for field, values in many_field.items():

                for value in values:

                    getattr(instance, field).add( value )


        return {
            'instance': instance,
            'kwargs': kwargs,
            'api_json': ''
        }


    yield data