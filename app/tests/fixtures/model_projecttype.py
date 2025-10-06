import pytest
import random

from project_management.models.project_types import ProjectType
from project_management.serializers.project_type import (
    ProjectTypeBaseSerializer,
    ProjectTypeModelSerializer,
    ProjectTypeViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_projecttype(clean_model_from_db):

    yield ProjectType

    clean_model_from_db(ProjectType)


@pytest.fixture( scope = 'class')
def kwargs_projecttype(kwargs_centurionmodel, django_db_blocker,
    model_projecttype,
    model_knowledgebase, kwargs_knowledgebase,
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_knowledgebase()
            team = kwargs['target_team']
            del kwargs['target_team']

            runbook = model_knowledgebase.objects.create( **kwargs )

            runbook.target_team.add( team[0] )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'projecttype_' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            'runbook': runbook,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_projecttype():

    yield {
        'base': ProjectTypeBaseSerializer,
        'model': ProjectTypeModelSerializer,
        'view': ProjectTypeViewSerializer
    }
