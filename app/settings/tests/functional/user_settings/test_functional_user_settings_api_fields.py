import pytest

from django.db import models

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_usersettings
class UserSettingsAPITestCases(
    APIFieldsInheritedCases,
):


    @pytest.fixture( scope = 'class')
    def create_model(self, request, django_db_blocker,
        model, model_kwargs, api_request_permissions
    ):

        item = None

        with django_db_blocker.unblock():

            item = model.objects.get(
                id = api_request_permissions['user']['view'].id
            )

            request.cls.item = item

        yield item



    @property
    def parameterized_api_fields(self):

        return {
            '_urls.notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.markdown': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.render': {
                'expected': models.NOT_PROVIDED
            },
            'organization': {
                'expected': models.NOT_PROVIDED
            },
            'organization.id': {
                'expected': models.NOT_PROVIDED
            },
            'organization.display_name': {
                'expected': models.NOT_PROVIDED
            },
            'organization.url': {
                'expected': models.NOT_PROVIDED
            },
            'user': {
                'expected': int
            },
            'user.id': {    # Must not exist as the pk is the user ID
                'expected': models.NOT_PROVIDED
            },
            'user.display_name': {    # Must not exist as the pk is the user ID
                'expected': models.NOT_PROVIDED
            },
            'user.url': {    # Must not exist as the pk is the user ID
                'expected': models.NOT_PROVIDED
            },
            'browser_mode': {    # Must not exist as the pk is the user ID
                'expected': int
            },
            # 'default_organization': {    # Not yet required
            #     'expected': dict
            # },
            # 'default_organization.id': {
            #     'expected': int
            # },
            # 'default_organization.display_name': {
            #     'expected': str
            # },
            # 'default_organization.url': {
            #     'expected': Hyperlink
            # },
            'timezone': {
                'expected': str
            },
            'modified': {
                'expected': str
            }
        }



class UserSettingsAPIInheritedCases(
    UserSettingsAPITestCases,
):
    pass



@pytest.mark.module_settings
class UserSettingsAPIPyTest(
    UserSettingsAPITestCases,
):

    pass
