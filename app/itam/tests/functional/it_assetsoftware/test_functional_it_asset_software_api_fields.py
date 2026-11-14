import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_itasset
class ITAssetSoftwareAPITestCases(
    APIFieldsInheritedCases,
):


    @pytest.fixture( scope = 'class')
    def api_request_permissions(self, api_request_permissions,
        django_db_blocker, model_kwargs, model_permission,
        model_contenttype,
    ):


        with django_db_blocker.unblock():

            amended_request_permissions = api_request_permissions.copy()

            kwargs = model_kwargs()

            parent_model = kwargs['it_asset']

            change_permission = model_permission.objects.get(
                    codename = 'change_' + parent_model._meta.model_name,
                    content_type = model_contenttype.objects.get(
                        app_label = parent_model._meta.app_label,
                        model = parent_model._meta.model_name,
                    )
                )

            amended_request_permissions['user']['add'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            amended_request_permissions['user']['change'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            amended_request_permissions['user']['delete'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            view_permission = model_permission.objects.get(
                    codename = 'view_' + parent_model._meta.model_name,
                    content_type = model_contenttype.objects.get(
                        app_label = parent_model._meta.app_label,
                        model = parent_model._meta.model_name,
                    )
                )

            amended_request_permissions['user']['view'].groups.all(
            ).first().roles.all().first().permissions.add(view_permission)


        yield amended_request_permissions


    @property
    def parameterized_api_fields(self):

        return {
            'it_asset': {
                'expected': dict
            },
            'it_asset.id': {
                'expected': int
            },
            'it_asset.display_name': {
                'expected': str
            },
            'it_asset.url': {
                'expected': str
            },
            'software': {
                'expected': dict
            },
            'software.id': {
                'expected': int
            },
            'software.display_name': {
                'expected': str
            },
            'software.url': {
                'expected': Hyperlink
            },
            'action': {
                'expected': int
            },
            'version': {
                'expected': dict
            },
            'version.id': {
                'expected': int
            },
            'version.display_name': {
                'expected': str
            },
            'version.url': {
                'expected': str
            },
            'installedversion': {
                'expected': dict
            },
            'installedversion.id': {
                'expected': int
            },
            'installedversion.display_name': {
                'expected': str
            },
            'installedversion.url': {
                'expected': str
            },
            'installed': {
                'expected': str
            },

            # fields dont exist as model is not centurion model.
            'display_name': {
                'expected': models.NOT_PROVIDED
            },
            '_urls.notes': {
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
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.markdown': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.render': {
                'expected': models.NOT_PROVIDED
            },
            'created': {
                'expected': models.NOT_PROVIDED
            },
            'modified': {
                'expected': models.NOT_PROVIDED
            },

        }



class ITAssetSoftwareAPIInheritedCases(
    ITAssetSoftwareAPITestCases,
):

    pass



@pytest.mark.module_itam
class ITAssetSoftwareAPIPyTest(
    ITAssetSoftwareAPITestCases,
):

    pass
