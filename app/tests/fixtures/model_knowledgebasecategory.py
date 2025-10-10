import pytest
import random

from assistance.models.knowledge_base_category import KnowledgeBaseCategory
from assistance.serializers.knowledge_base_category import (
    KnowledgeBaseCategoryBaseSerializer,
    KnowledgeBaseCategoryModelSerializer,
    KnowledgeBaseCategoryViewSerializer
)



@pytest.fixture( scope = 'class')
def model_knowledgebasecategory(clean_model_from_db):

    yield KnowledgeBaseCategory

    clean_model_from_db(KnowledgeBaseCategory)


@pytest.fixture( scope = 'class')
def kwargs_knowledgebasecategory(django_db_blocker, kwargs_centurionmodel, model_user):

    def factory():

        with django_db_blocker.unblock():

            random_str = str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299))

            user = model_user.objects.create(
                username = 'kb cat tgt user' + random_str,
                password = 'apassword'
            )

            kwargs = {
                **kwargs_centurionmodel(),
                'name': 'kb cat' + random_str,
                # 'parent_category': '',
                # 'target_team': '',
                'target_user': user,
                'modified': '2024-06-03T23:00:00Z',
            }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_knowledgebasecategory():

    yield {
        'base': KnowledgeBaseCategoryBaseSerializer,
        'model': KnowledgeBaseCategoryModelSerializer,
        'view': KnowledgeBaseCategoryViewSerializer
    }
