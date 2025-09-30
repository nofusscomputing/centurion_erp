import pytest
import random

from django.db import models

from project_management.models.project_milestone import ProjectMilestone
from project_management.serializers.project_milestone import (
    ProjectMilestoneBaseSerializer,
    ProjectMilestoneModelSerializer,
    ProjectMilestoneViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_projectmilestone(clean_model_from_db):

    yield ProjectMilestone

    clean_model_from_db(ProjectMilestone)


@pytest.fixture( scope = 'class')
def kwargs_projectmilestone(django_db_blocker,
    kwargs_centurionmodel, kwargs_project, model_project,
):

    def factory():

        with django_db_blocker.unblock():

            kwargs_many_to_many = {}

            kwargs = {}

            for key, value in kwargs_project().items():

                field = model_project._meta.get_field(key)

                if isinstance(field, models.ManyToManyField):

                    kwargs_many_to_many.update({
                        key: value
                    })

                else:

                    kwargs.update({
                        key: value
                    })

            kwargs.update({
                'name': 'pm' + str( random.randint(1,99) ) + str( random.randint(100,199) ) + str( random.randint(200,299) )
            })
            del kwargs['code']

            project = model_project.objects.create(
                **kwargs
            )


        kwargs = kwargs_centurionmodel()
        del kwargs['model_notes']

        kwargs = {
            **kwargs,
            'name': 'pm_' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            'project': project,
            'start_date': '2025-08-04T00:00:01Z',
            'finish_date': '2025-08-04T00:00:02Z',
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_projectmilestone():

    yield {
        'base': ProjectMilestoneBaseSerializer,
        'model': ProjectMilestoneModelSerializer,
        'view': ProjectMilestoneViewSerializer
    }
