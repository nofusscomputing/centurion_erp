import pytest
import random

from datetime import datetime

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

    def factory():

        with django_db_blocker.unblock():

            random_str = str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

            group = model_group.objects.create(
                name = 'kb tgt team' + random_str
            )

            user = model_user.objects.create(
                username = 'kb resp user' + random_str,
                password = 'apassword'
            )

            category = model_knowledgebasecategory.objects.create(
                organization = kwargs_centurionmodel()['organization'],
                name = 'kb cat for kb art' + random_str
            )

            kwargs = {
                **kwargs_centurionmodel(),
                'title': 'title' + random_str,
                'summary': 'a summary',
                'content': 'the kb body text',
                'category': category,
                'release_date': (
                    f'2024-{random.randint(1, 12):02d}'
                    f'-{random.randint(1, 28):02d}'
                    f'T{random.randint(0, 23):02d}:'
                    f'{random.randint(0, 59):02d}:'
                    f'{random.randint(0, 59):02d}Z'
                ),
                'expiry_date': (
                    f'2024-{random.randint(1, 12):02d}'
                    f'-{random.randint(1, 28):02d}'
                    f'T{random.randint(0, 23):02d}:'
                    f'{random.randint(0, 59):02d}:'
                    f'{random.randint(0, 59):02d}Z'
                ),
                'target_team': [ group ],
                # 'target_user': ,
                'responsible_user': user,
                # 'responsible_teams': '',
                'public': True,
            }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_knowledgebase():

    yield {
        'base': KnowledgeBaseBaseSerializer,
        'model': KnowledgeBaseModelSerializer,
        'view': KnowledgeBaseViewSerializer
    }
