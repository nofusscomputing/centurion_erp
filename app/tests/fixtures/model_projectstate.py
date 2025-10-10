import pytest
import random

from project_management.models.project_states import ProjectState
from project_management.serializers.project_states import (
    ProjectStateBaseSerializer,
    ProjectStateModelSerializer,
    ProjectStateViewSerializer,
)


@pytest.fixture( scope = 'class')
def model_projectstate(clean_model_from_db):

    yield ProjectState

    clean_model_from_db(ProjectState)


@pytest.fixture( scope = 'class')
def kwargs_projectstate(kwargs_centurionmodel, django_db_blocker,
    model_knowledgebase, kwargs_knowledgebase,
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_knowledgebase()
            team = kwargs['target_team']
            del kwargs['target_team']

            runbook = model_knowledgebase.objects.create( **kwargs )

            runbook.target_team.add( team[0] )

        kwargs = kwargs_centurionmodel()

        kwargs = {
            **kwargs,
            'name': 'projectstate_' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            'runbook': runbook,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_projectstate():

    yield {
        'base': ProjectStateBaseSerializer,
        'model': ProjectStateModelSerializer,
        'view': ProjectStateViewSerializer
    }
