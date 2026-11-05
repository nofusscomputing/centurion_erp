import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_itasset
class ITAssetAPITestCases(
    APIFieldsInheritedCases,
):


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



class ITAssetAPIInheritedCases(
    ITAssetAPITestCases,
):

    pass



@pytest.mark.module_itam
class ITAssetAPIPyTest(
    ITAssetAPITestCases,
):

    pass
