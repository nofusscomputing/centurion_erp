import datetime
import pytest

from assistance.models.knowledge_base_category import KnowledgeBaseCategory



@pytest.fixture( scope = 'class')
def model_knowledgebasecategory():

    yield KnowledgeBaseCategory


@pytest.fixture( scope = 'class')
def kwargs_knowledgebasecategory(django_db_blocker, kwargs_centurionmodel, model_user):

    with django_db_blocker.unblock():

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

        user = model_user.objects.create(
            username = 'kb cat tgt user' + random_str,
            password = 'apassword'
        )

        kwargs = {
            **kwargs_centurionmodel.copy(),
            'name': 'kb cat' + random_str,
            # 'parent_category': '',
            # 'target_team': '',
            'target_user': user,
            'modified': '2024-06-03T23:00:00Z',
        }

        yield kwargs.copy()

        user.delete()
