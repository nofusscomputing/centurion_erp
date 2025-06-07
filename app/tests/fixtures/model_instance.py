import datetime
import pytest

from django.apps import apps
from django.db import models



model_objs: list = []


@pytest.fixture( scope = 'class')
def model_instance(django_db_blocker, model_user, model, model_kwargs):

    with django_db_blocker.unblock():


        def instance( random_field:str = '', kwargs_create: dict = {} ):
            """Create a model instance

            Args:
                random_field (str, optional): The unique field that needs to be randomized.
                    Defaults to ''.
                kwargs_create (dict, optional): object create kwargs. overwrites default.
                    Defaults to {}.

            Returns:
                Model Object (Model): Model that was created.
            """

            global model_objs

            obj = None


            if model._meta.abstract:

                class MockModel(model):
                    class Meta:
                        app_label = 'core'
                        verbose_name = 'mock instance'
                        managed = False

                obj = MockModel()


                if 'mockmodel' in apps.all_models['core']:

                    del apps.all_models['core']['mockmodel']


            else:

                new_kwargs = model_kwargs.copy()

                new_kwargs.update( kwargs_create )


                kwargs = {}

                many_field = {}

                for field, value in new_kwargs.items():

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

                    kwargs.update({
                        field: value
                    })


                if random_field:

                    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

                    kwargs.update({
                        random_field: str( random_field ) + '_' + random_str
                    })


                obj = model.objects.create(
                    **kwargs
                )

            for field, values in many_field.items():

                for value in values:

                    getattr(obj, field).add( value )


            model_objs += [ obj ]

            return obj

    yield instance

    with django_db_blocker.unblock():

        for model_obj in model_objs:

            if model_obj._meta.abstract:

                del model_obj

            else:

                try:
                    model_obj.delete()
                except:
                    pass


    if 'mockmodel' in apps.all_models['core']:

        del apps.all_models['core']['mockmodel']
