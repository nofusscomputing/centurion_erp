import datetime
import pytest

from assistance.models.knowledge_base import KnowledgeBase



@pytest.fixture( scope = 'class')
def model_knowledgebase():

    yield KnowledgeBase


@pytest.fixture( scope = 'class')
def kwargs_knowledgebase(django_db_blocker, 
    kwargs_centurionmodel, model_team, model_user, model_knowledgebasecategory
):


    with django_db_blocker.unblock():

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

        team = model_team.objects.create(
            organization = kwargs_centurionmodel['organization'],
            team_name = 'kb tgt team' + random_str
        )

        user = model_user.objects.create(
            username = 'kb resp user' + random_str,
            password = 'apassword'
        )

        category = model_knowledgebasecategory.objects.create(
            organization = kwargs_centurionmodel['organization'],
            name = 'kb cat for kb art' + random_str
        )

        kwargs = {
            **kwargs_centurionmodel.copy(),
            'title': 'title' + random_str,
            'summary': 'a summary',
            'content': 'the kb body text',
            'category': category,
            'release_date': '2024-06-04T00:00:01Z',
            'expiry_date': '2024-06-04T00:00:02Z',
            'target_team': [ team ],
            # 'target_user': ,
            'responsible_user': user,
            # 'responsible_teams': '',
            'public': True,
            'modified': '2024-06-03T23:00:00Z',
        }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        team.delete()

        try:

            user.delete()
        except:
            pass

        category.delete()
