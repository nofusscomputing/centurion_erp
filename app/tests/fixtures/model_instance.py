import datetime
import pytest

from django.apps import apps



model_objs: list = []


@pytest.fixture( scope = 'class')
def model_instance(django_db_blocker, model_user, model, model_kwargs):

    with django_db_blocker.unblock():


        def instance( user = None, random_field:str = '', kwargs_create: dict = {} ):
            """Create a model instance

            Args:
                user (User, optional): The User to create and add to model.context['user'].
                    Defaults to None.
                random_field (str, optional): The unique field that needs to be randomized.
                    Defaults to ''.
                kwargs_create (dict, optional): object create kwargs. overwrites default.
                    Defaults to {}.

            Returns:
                Model Object (Model): Model that was created.
            """

            global model_objs

            obj = None

            if user:
                model.context['user'] = user


            if model._meta.abstract:

                class MockModel(model):
                    class Meta:
                        app_label = 'core'
                        verbose_name = 'mock instance'
                        managed = False

                obj = MockModel()

            else:

                kwargs = model_kwargs.copy()

                kwargs.update( kwargs_create )

                if random_field:

                    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

                    kwargs.update({
                        random_field: str( random_field ) + '_' + random_str
                    })

                obj = model.objects.create(
                    **kwargs
                )

            model_objs += [ obj ]

            return obj

        yield instance

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
