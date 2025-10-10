import pytest
import random

from core.models.audit import CenturionAudit



@pytest.fixture( scope = 'class')
def model_centurionaudit(clean_model_from_db):

    yield CenturionAudit

    clean_model_from_db(CenturionAudit)


@pytest.fixture( scope = 'class')
def kwargs_centurionaudit(django_db_blocker,
    kwargs_centurionmodel, model_contenttype,
    kwargs_user, model_user
):

    def factory():

        kwargs = kwargs_centurionmodel()
        del kwargs['model_notes']

        with django_db_blocker.unblock():


            random_str = str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299))

            user_kwargs = kwargs_user()
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
                'content_type': model_contenttype.objects.get(
                    app_label = user._meta.app_label,
                    model = user._meta.model_name,
                ),
            }

        return kwargs

    yield factory
