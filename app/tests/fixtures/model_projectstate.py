import datetime
import pytest

from django.db import models

from project_management.models.project_states import ProjectState
from project_management.serializers.project_states import (
    ProjectStateBaseSerializer,
    ProjectStateModelSerializer,
    ProjectStateViewSerializer,
)


@pytest.fixture( scope = 'class')
def model_projectstate():

    yield ProjectState


@pytest.fixture( scope = 'class')
def kwargs_projectstate(kwargs_centurionmodel, django_db_blocker,
    model_knowledgebase, kwargs_knowledgebase,
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        kwargs = kwargs_knowledgebase.copy()
        team = kwargs['target_team']
        del kwargs['target_team']

        runbook = model_knowledgebase.objects.create( **kwargs )

        runbook.target_team.add( team[0] )

    kwargs = kwargs_centurionmodel.copy()

    kwargs = {
        **kwargs,
        'name': 'projectstate_' + random_str,
        'runbook': runbook,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        for proj in runbook.projectstate_set.all():
            proj.delete()

        runbook.delete()



@pytest.fixture( scope = 'class')
def serializer_projectstate():

    yield {
        'base': ProjectStateBaseSerializer,
        'model': ProjectStateModelSerializer,
        'view': ProjectStateViewSerializer
    }
