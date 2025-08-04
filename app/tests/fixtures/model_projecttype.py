import datetime
import pytest

from django.db import models

from project_management.models.project_types import ProjectType
from project_management.serializers.project_type import (
    ProjectTypeBaseSerializer,
    ProjectTypeModelSerializer,
    ProjectTypeViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_projecttype():

    yield ProjectType


@pytest.fixture( scope = 'class')
def kwargs_projecttype(kwargs_centurionmodel, django_db_blocker,
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

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'projecttype_' + random_str,
        'runbook': runbook,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        try:
            runbook.delete()
        except models.deletion.ProtectedError:
            pass


@pytest.fixture( scope = 'class')
def serializer_projecttype():

    yield {
        'base': ProjectTypeBaseSerializer,
        'model': ProjectTypeModelSerializer,
        'view': ProjectTypeViewSerializer
    }
