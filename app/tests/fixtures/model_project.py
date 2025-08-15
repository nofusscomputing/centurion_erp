import datetime
import pytest
import random

from django.db import models

from project_management.models.projects import Project
from project_management.serializers.project import (
    ProjectBaseSerializer,
    ProjectImportSerializer,
    ProjectModelSerializer,
    ProjectViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_project():

    yield Project


@pytest.fixture( scope = 'class')
def kwargs_project(kwargs_centurionmodel, django_db_blocker,
    model_projectstate, kwargs_projectstate,
    model_projecttype, kwargs_projecttype,
    model_user, kwargs_user,
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        state = model_projectstate.objects.create( **kwargs_projectstate )

        pr_type = model_projecttype.objects.create( **kwargs_projecttype )

        kwargs = kwargs_user.copy()
        kwargs['username'] = 'tm_proj' + str( random.randint(333, 666) )
        manager = model_user.objects.create( **kwargs )

        kwargs = kwargs_user.copy()
        kwargs['username'] = 'tm_proj' + str( random.randint(777, 999) )
        team_member = model_user.objects.create( **kwargs )

    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    kwargs = {
        **kwargs,
        'code': 'aCODE',
        'name': 'project_' + random_str,
        'description': 'a description',
        'priority': Project.Priority.LOW,
        'state': state,
        'project_type': pr_type,
        'planned_start_date': '2025-08-04T00:00:01Z',
        'planned_finish_date': '2025-08-04T00:00:02Z',
        'real_start_date': '2025-08-04T00:00:03Z',
        'real_finish_date': '2025-08-04T00:00:04Z',
        'manager_user': manager,
        'team_members': [ team_member ],
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        try:
            state.delete()
        except models.deletion.ProtectedError:
            pass

        try:
            pr_type.delete()
        except models.deletion.ProtectedError:
            pass

        try:
            manager.delete()
        except models.deletion.ProtectedError:
            pass

        try:
            team_member.delete()
        except models.deletion.ProtectedError:
            pass



@pytest.fixture( scope = 'class')
def serializer_project():

    yield {
        'base': ProjectBaseSerializer,
        'import': ProjectImportSerializer,
        'model': ProjectModelSerializer,
        'view': ProjectViewSerializer
    }
