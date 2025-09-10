import datetime
import pytest

from core.models.centurion_notes import CenturionModelNote



@pytest.fixture( scope = 'class')
def model_centurionmodelnote(clean_model_from_db):

    yield CenturionModelNote

    clean_model_from_db(CenturionModelNote)


@pytest.fixture( scope = 'class')
def kwargs_centurionmodelnote(django_db_blocker,
    model_contenttype, kwargs_centurionmodel, kwargs_user, model_user):

    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    with django_db_blocker.unblock():

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

        user_kwargs = kwargs_user.copy()
        user_kwargs.update({
                'username': 'note_user' + str(random_str)
            })

        user = model_user.objects.create(
            **user_kwargs,
        )

        kwargs = {
            **kwargs,
            'body': 'a random note',
            'created_by': user,
            'content_type': model_contenttype.objects.get(
                app_label = user._meta.app_label,
                model = user._meta.model_name,
            ),
        }

    yield kwargs.copy()

    with django_db_blocker.unblock():
        user.delete()