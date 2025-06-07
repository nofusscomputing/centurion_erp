import datetime
import pytest

from django.apps import apps
from django.db import models



model_objs: list = []


@pytest.fixture( scope = 'class')
def model_instance(django_db_blocker, model_kwarg_data, model, model_kwargs):

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


                obj = model_kwarg_data(
                    model = model,
                    model_kwargs = model_kwargs,
                    create_instance = True,
                )

                obj = obj['instance']



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
