import pytest

from datetime import datetime

from core.models.centurion_notes import CenturionModelNote



@pytest.fixture( scope = 'class')
def model_centurionmodelnote(clean_model_from_db):

    yield CenturionModelNote

    clean_model_from_db(CenturionModelNote)


@pytest.fixture( scope = 'class')
def kwargs_centurionmodelnote(django_db_blocker,
    model_contenttype, kwargs_centurionmodel, kwargs_user, model_user):

    def factory():

        kwargs = kwargs_centurionmodel()
        del kwargs['model_notes']

        with django_db_blocker.unblock():

            user_kwargs = kwargs_user()
            user_kwargs.update({
                    'username': 'note_user' +  str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )
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

        return kwargs

    yield factory
