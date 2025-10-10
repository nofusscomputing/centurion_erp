import pytest

from django.apps import apps

from access.models.tenant import Tenant




@pytest.fixture( scope = 'function')
def model_instance(django_db_blocker, model_kwarg_data, model, model_kwargs, clean_model_from_db):

    with django_db_blocker.unblock():


        def instance(
            random_field:str = '',
            kwargs_create: dict = {},
            model_kwargs = model_kwargs
        ):
            """Create a model instance

            Args:
                random_field (str, optional): The unique field that needs to be randomized.
                    Defaults to ''.
                kwargs_create (dict, optional): object create kwargs. overwrites default.
                    Defaults to {}.

            Returns:
                Model Object (Model): Model that was created.
            """

            obj = None
            org = None

            model_kwargs = model_kwargs()

            kwargs = model_kwargs.copy()


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
                    model is Tenant
                    or (
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

                else:

                    obj = org

            if not obj:
                raise ValueError('no model created')

            return obj

    yield instance



    if 'mockmodel' in apps.all_models['core']:

        del apps.all_models['core']['mockmodel']
