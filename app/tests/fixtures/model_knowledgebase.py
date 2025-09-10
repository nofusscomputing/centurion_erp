import datetime
import pytest

from django.db import models

from assistance.models.knowledge_base import KnowledgeBase
from assistance.serializers.knowledge_base import (
    KnowledgeBaseBaseSerializer,
    KnowledgeBaseModelSerializer,
    KnowledgeBaseViewSerializer
)



@pytest.fixture( scope = 'class')
def model_knowledgebase(clean_model_from_db):

    yield KnowledgeBase

    clean_model_from_db(KnowledgeBase)


@pytest.fixture( scope = 'class')
def kwargs_knowledgebase(django_db_blocker, 
    kwargs_centurionmodel, model_group, model_user, model_knowledgebasecategory
):


    with django_db_blocker.unblock():

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

        group = model_group.objects.create(
            name = 'kb tgt team' + random_str
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
            'target_team': [ group ],
            # 'target_user': ,
            'responsible_user': user,
            # 'responsible_teams': '',
            'public': True,
            'modified': '2024-06-03T23:00:00Z',
        }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        group.delete()

        try:

            user.delete()
        except models.deletion.ProtectedError:
            pass

        try:
            category.delete()
        except models.deletion.ProtectedError:
            pass



@pytest.fixture( scope = 'class')
def serializer_knowledgebase():

    yield {
        'base': KnowledgeBaseBaseSerializer,
        'model': KnowledgeBaseModelSerializer,
        'view': KnowledgeBaseViewSerializer
    }
