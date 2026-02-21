import pytest
import random

from project_management.models.projects import Project
from project_management.serializers.project import (
    ProjectBaseSerializer,
    ProjectImportSerializer,
    ProjectModelSerializer,
    ProjectViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_project(clean_model_from_db):

    yield Project

    clean_model_from_db(Project)


@pytest.fixture( scope = 'class')
def kwargs_project(kwargs_centurionmodel, django_db_blocker,
    model_projectstate, kwargs_projectstate,
    model_projecttype, kwargs_projecttype,
    model_user, kwargs_user,
):

    def factory():

        with django_db_blocker.unblock():

            state = model_projectstate.objects.create( **kwargs_projectstate() )

            pr_type = model_projecttype.objects.create( **kwargs_projecttype() )

            kwargs = kwargs_user()
            kwargs['username'] = 'tm_man_proj' + str( random.randint(333, 666) ) + str( random.randint(333, 666) ) + str( random.randint(333, 666) )
            manager = model_user.objects.create( **kwargs )

            kwargs = kwargs_user()
            kwargs['username'] = 'tm_proj' + str( random.randint(777, 999) ) + str( random.randint(333, 666) ) + str( random.randint(333, 666) )
            team_member = model_user.objects.create( **kwargs )

        kwargs = kwargs_centurionmodel()
        del kwargs['model_notes']

        kwargs = {
            **kwargs,
            'code': 'aCODE' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            'name': 'project_' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            'description': 'a description',
            'priority': Project.Priority.LOW,
            'state': state,
            'project_type': pr_type,
            'planned_start_date': (
                f'2025-{random.randint(1, 12):02d}'
                f'-{random.randint(1, 28):02d}'
                f'T{random.randint(0, 23):02d}:'
                f'{random.randint(0, 59):02d}:'
                f'{random.randint(0, 59):02d}Z'
            ),
            'planned_finish_date': (
                f'2025-{random.randint(1, 12):02d}'
                f'-{random.randint(1, 28):02d}'
                f'T{random.randint(0, 23):02d}:'
                f'{random.randint(0, 59):02d}:'
                f'{random.randint(0, 59):02d}Z'
            ),
            'real_start_date': (
                f'2025-{random.randint(1, 12):02d}'
                f'-{random.randint(1, 28):02d}'
                f'T{random.randint(0, 23):02d}:'
                f'{random.randint(0, 59):02d}:'
                f'{random.randint(0, 59):02d}Z'
            ),
            'real_finish_date': (
                f'2025-{random.randint(1, 12):02d}'
                f'-{random.randint(1, 28):02d}'
                f'T{random.randint(0, 23):02d}:'
                f'{random.randint(0, 59):02d}:'
                f'{random.randint(0, 59):02d}Z'
            ),
            'manager_user': manager,
            'team_members': [ team_member ],
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_project():

    yield {
        'base': ProjectBaseSerializer,
        'import': ProjectImportSerializer,
        'model': ProjectModelSerializer,
        'view': ProjectViewSerializer
    }
