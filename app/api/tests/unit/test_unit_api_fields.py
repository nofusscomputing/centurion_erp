import pytest

from django.contrib.auth.models import ContentType, Permission, User
from django.shortcuts import reverse
from django.test import Client

from rest_framework.relations import Hyperlink

from access.models.team import Team
from access.models.team_user import TeamUsers

from app.tests.common import DoesNotExist



class APIFieldsTestCases:
    
    api_fields_common = {
        'id': {
            'expected': int
        },
        'display_name': {
            'expected': str
        },
        '_urls': {
            'expected': dict
        },
        '_urls._self': {
            'expected': str
        },
        '_urls.notes': {
            'expected': str
        },
    }

    api_fields_model = {
        'model_notes': {
            'expected': str
        },
        'created': {
            'expected': str
        },
        'modified': {
            'expected': str
        },
    }

    api_fields_tenancy = {
        'organization': {
            'expected': dict
        },
        'organization.id': {
            'expected': int
        },
        'organization.display_name': {
            'expected': str
        },
        'organization.url': {
            'expected': Hyperlink
        },
    }

    parametrized_test_data = {
        **api_fields_common,
        **api_fields_tenancy,
        **api_fields_model,
    }

    url_view_kwargs = {}



    @pytest.fixture( scope = 'class')
    def setup_pre(self,
        request,
        model,
        django_db_blocker,
        organization_one,
        organization_two
    ):

        with django_db_blocker.unblock():

            request.cls.organization = organization_one

            request.cls.different_organization = organization_two

            kwargs_create_item = {}

            for base in reversed(request.cls.__mro__):

                if hasattr(base, 'kwargs_create_item'):

                    if base.kwargs_create_item is None:

                        continue

                    kwargs_create_item.update(**base.kwargs_create_item)


            if len(kwargs_create_item) > 0:

                request.cls.kwargs_create_item = kwargs_create_item


            if 'organization' not in request.cls.kwargs_create_item:

                request.cls.kwargs_create_item.update({
                    'organization': request.cls.organization
                })

            view_permissions = Permission.objects.get(
                    codename = 'view_' + request.cls.model._meta.model_name,
                    content_type = ContentType.objects.get(
                        app_label = request.cls.model._meta.app_label,
                        model = request.cls.model._meta.model_name,
                    )
                )

            view_team = Team.objects.create(
                team_name = 'cs_api_view_team',
                organization = request.cls.organization,
            )

            view_team.permissions.set([view_permissions])


            request.cls.view_user = User.objects.create_user(username="cafs_test_user_view", password="password")

            team_user = TeamUsers.objects.create(
                team = view_team,
                user = request.cls.view_user
            )

        yield

        with django_db_blocker.unblock():

            team_user.delete()

            view_team.delete()

            request.cls.view_user.delete()

            del request.cls.kwargs_create_item


    @pytest.fixture( scope = 'class')
    def setup_post(self, request, django_db_blocker):

        with django_db_blocker.unblock():

            request.cls.url_view_kwargs.update({
                'pk': request.cls.item.id
            })

            client = Client()
            url = reverse('v2:' + request.cls.url_ns_name + '-detail', kwargs=request.cls.url_view_kwargs)


            client.force_login(request.cls.view_user)
            response = client.get(url)

            request.cls.api_data = response.data

        yield

        del request.cls.url_view_kwargs['pk']




    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_pre,
        create_model,
        setup_post,
    ):

        pass


    def test_api_field_exists(self, recursearray, parameterized, param_key_test_data,
        param_value,
        param_expected
    ):
        """Test for existance of API Field"""

        api_data = recursearray(self.api_data, param_value)

        if param_expected is DoesNotExist:

            assert api_data['key'] not in api_data['obj']

        else:

            assert api_data['key'] in api_data['obj']



    def test_api_field_type(self, recursearray, parameterized, param_key_test_data,
        param_value,
        param_expected
    ):
        """Test for type for API Field"""

        api_data = recursearray(self.api_data, param_value)

        if param_expected is DoesNotExist:

            assert api_data['key'] not in api_data['obj']

        else:

            assert type( api_data['value'] ) is param_expected



class APIFieldsInheritedCases(
    APIFieldsTestCases
):

    model = None
