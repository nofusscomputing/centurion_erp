import pytest


from django.db.models.deletion import ProtectedError


@pytest.fixture( scope = 'class')
def clean_model_from_db(django_db_blocker):


    def clean_db(model_to_clean):

        with django_db_blocker.unblock():

            if model_to_clean._meta.abstract:
                return

            for db_obj in model_to_clean.objects.all():

                if db_obj._meta.model_name == 'appsettings':
                    if db_obj.owner_organization is None:
                        continue

                for linked_model in db_obj._meta.related_objects:

                    for rel_obj in linked_model.related_model.objects.all():

                        if rel_obj._meta.model_name == 'appsettings':
                            if rel_obj.owner_organization is None:
                                continue

                        try:
                            rel_obj.delete()
                        except ProtectedError:
                            pass

                try:
                    db_obj.delete()
                except ProtectedError:
                    pass

    yield clean_db
