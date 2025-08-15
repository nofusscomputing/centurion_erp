import datetime
import pytest

from django.apps import apps
from django.db import models

from access.models.tenant import Tenant



model_objs: list = []


@pytest.fixture( scope = 'function')
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
            org = None

            kwargs = model_kwargs

            if kwargs_create:

                if(
                    'organization' in kwargs_create
                    and type(model) is not Tenant
                ):

                    org = kwargs_create['organization']

                elif(
                    'organization' in kwargs_create
                    and type(model) is  Tenant
                ):

                    # org = kwargs_create['organization']

                    del kwargs_create['organization']

                kwargs.update(
                    **kwargs_create
                )



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


                if(
                    model is not Tenant
                    and (
                        org is not None
                        or (
                            'organization' not in model_kwargs
                            and 'organization' not in kwargs_create
                        )
                    )
                ):

                    obj = model_kwarg_data(
                        model = model,
                        model_kwargs = kwargs,
                        create_instance = True,
                    )

                    obj = obj['instance']

                    model_objs += [ obj ]

                else:

                    obj = org


            return obj

    yield instance

    with django_db_blocker.unblock():

        for model_obj in model_objs:

            is_abstract = False

            if hasattr(model_obj, '_meta'):

                is_abstract = model_obj._meta.abstract


            if is_abstract:

                del model_obj

            else:

                try:
                    model_obj.delete()
                except:
                    pass


    if 'mockmodel' in apps.all_models['core']:

        del apps.all_models['core']['mockmodel']
