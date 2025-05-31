import datetime
import pytest

from core.models.audit import CenturionAudit



@pytest.fixture( scope = 'class')
def model_centurionaudit():

    yield CenturionAudit


@pytest.fixture( scope = 'class')
def kwargs_centurionaudit(django_db_blocker, kwargs_centurionmodel, kwargs_user, model_user):

    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    with django_db_blocker.unblock():


        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

        user_kwargs = kwargs_user.copy()
        user_kwargs.update({
                'username': 'audit_user' + str(random_str)
            })

        user = model_user.objects.create(
            **user_kwargs,
        )

        kwargs = {
            **kwargs,
            'before': {},
            'after': {
                'after_key': 'after_value'
            },
            'action': CenturionAudit.Actions.ADD,
            'user': user,
            'content_type': 'fixture sets value',
        }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        user.delete()
