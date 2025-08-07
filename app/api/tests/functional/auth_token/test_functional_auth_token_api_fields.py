import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_authtoken
class AuthTokenAPITestCases(
    APIFieldsInheritedCases,
):


    @pytest.fixture( scope = 'class')
    def create_model(self, request, django_db_blocker,
        model, model_kwargs, api_request_permissions,
    ):

        item = None

        with django_db_blocker.unblock():

            kwargs = model_kwargs.copy()
            kwargs['user'] = api_request_permissions['user']['view']


            item = model.objects.create(
                **kwargs
            )

            request.cls.item = item

        yield item

        with django_db_blocker.unblock():

            item.delete()


    @property
    def parameterized_api_fields(self):

        return {
            '_urls.notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            'id': {
                'expected': int
            },
            'note': {
                'expected': str
            },
            'token': {    # Must not be in fields
                'expected': models.NOT_PROVIDED
            },
            'user': {
                'expected': int
            },
            'user.id': {    # Must not be in fields as object belongs to user requesting
                'expected': models.NOT_PROVIDED
            },
            'user.display_name': {    # Must not be in fields as object belongs to user requesting
                'expected': models.NOT_PROVIDED
            },
            'user.url': {    # Must not be in fields as object belongs to user requesting
                'expected': models.NOT_PROVIDED
            },
            'organization': {    # Not a tenancy model
                'expected': models.NOT_PROVIDED
            },
            'organization.id': {    # Not a tenancy model
                'expected': models.NOT_PROVIDED
            },
            'organization.display_name': {    # Not a tenancy model
                'expected': models.NOT_PROVIDED
            },
            'organization.url': {    # Not a tenancy model
                'expected': models.NOT_PROVIDED
            },
            'expires': {
                'expected': str
            },
            'created': {
                'expected': str
            },
            'modified': {
                'expected': str
            }
        }



class AuthTokenAPIInheritedCases(
    AuthTokenAPITestCases,
):
    pass



@pytest.mark.module_api
class AuthTokenAPIPyTest(
    AuthTokenAPITestCases,
):

    pass
