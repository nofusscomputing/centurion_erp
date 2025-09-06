import datetime
import pytest
import random

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from django.db import models


@pytest.fixture( scope = 'class' )
def model_kwarg_data():

    def data(model, model_kwargs, model_instance = None, create_instance = False) -> dict:

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
        random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '').replace('-', '')


        kwargs = {}

        many_field = {}

        for field, value in model_kwargs.items():

            is_unique_together_field = False
            
            if not hasattr(model, field):
                continue

            if not hasattr(getattr(model, field), 'field'):
                continue

            for unique_field in getattr(model, field).field.model._meta.unique_together:

                if field in unique_field and getattr(model, field).field.choices is None:

                    is_unique_together_field = True

            if isinstance(getattr(model, field).field, models.ManyToManyField):

                if isinstance(value, list):

                    value_list = []

                    for list_value in value:

                        if isinstance(list_value, models.Model):
                            value_list += [ list_value.id ]

                    value = value_list


                if field in many_field:

                    many_field[field] += [ value ]

                elif isinstance(value, list):

                    many_field.update({
                        field: value
                    })

                else:

                    many_field.update({
                        field: [
                            value
                        ]
                    })

                continue

            elif(
                (
                    getattr(model, field).field.unique
                    or is_unique_together_field
                )
                and not isinstance(getattr(model, field).field, models.UUIDField)
                and not isinstance(getattr(model, field).field, models.ForeignKey)

            ):

                value = 'a' + str(random.randint(1,999))

                if isinstance(getattr(model, field).field, models.IntegerField):

                    # value = str(random_str)[( len(random_str) - 13 ):]
                    value = random.randint(1,999999)

                elif isinstance(getattr(model, field).field, models.EmailField):


                    value = str(random.randint(1,999)) + '@instance.tld'

            elif isinstance(getattr(model, field).field, models.UUIDField):


                value = '6318f7cc-e3e8-4680-a3bf-29d77ce' + str( random.randint(20000, 99999) )

            elif(
                isinstance(getattr(model, field).field, models.DateField)
                and field not in [ 'created', 'modified' ]
            ):


                value = str(random.randint(1972, 2037)) + '-' + str(
                    random.randint(1, 12)) + '-' + str(random.randint(1, 28))


            kwargs.update({
                field: value
            })

        instance = None

        if create_instance:

            try:

                instance =model.objects.create(
                    **kwargs
                )

            except ValidationError as e:

                if '__all__' in e.error_dict:

                    if 'unique' in e.error_dict['__all__'][0].code:

                        try:

                            instance = model.objects.get(
                                **kwargs
                            )

                        except ObjectDoesNotExist as e:

                            if 'modified' in kwargs:

                                no_modified_in_kwargs = kwargs.copy()
                                del no_modified_in_kwargs['modified']

                                instance = model.objects.get(
                                    **no_modified_in_kwargs
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