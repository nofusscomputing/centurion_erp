import datetime
import django
import pytest

from django.contrib.auth.models import ContentType, Permission
from django.shortcuts import reverse
from django.test import Client

from rest_framework.relations import Hyperlink

from access.models.team import Team
from access.models.team_user import TeamUsers

from centurion.tests.common import DoesNotExist

User = django.contrib.auth.get_user_model()



class APIFieldsTestCases:
    """ API field Rendering Test Suite

    This test suite tests the rendering of API fieilds.

    ## Additional Items

    You may find a scenario where you are unable to have all fileds available
    within a single request. to overcome this this test suite has the features
    available wherein you can prepare an additional item for an additional
    check. the following is required before the API request is made
    (setup_post fixture):

    - additional item created and stored in attribute `self.item_two`
    - additional url as a string and stored in attribute `self.url_two`

    Once you have these two objects, an additional check will be done and each
    test will check both API requests. if the field is found in either api
    request the test will pass
    """

    @property
    def parameterized_test_data(self) -> dict:

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

        return {
            **api_fields_common.copy(),
            **api_fields_tenancy.copy(),
            **api_fields_model.copy(),
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

        request.cls.url_view_kwargs = {}
        request.cls.model = model

        with django_db_blocker.unblock():

            random_str = datetime.datetime.now(tz=datetime.timezone.utc)

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


            if hasattr(request.cls.model(), 'model_notes'):

                for field in request.cls.model()._meta.fields:

                    if field.attname == 'model_notes':

                        request.cls.kwargs_create_item.update({
                            'model_notes': 'notes',
                        })


            view_permissions = Permission.objects.get(
                    codename = 'view_' + request.cls.model._meta.model_name,
                    content_type = ContentType.objects.get(
                        app_label = request.cls.model._meta.app_label,
                        model = request.cls.model._meta.model_name,
                    )
                )

            view_team = Team.objects.create(
                team_name = 'cs_api_view_team' + str(random_str),
                organization = request.cls.organization,
            )

            request.cls.view_team = view_team

            view_team.permissions.set([view_permissions])

            request.cls.view_user = User.objects.create_user(username="cafs_test_user_view" + str(random_str), password="password", is_superuser = True)

            team_user = TeamUsers.objects.create(
                team = view_team,
                user = request.cls.view_user
            )

        yield

        with django_db_blocker.unblock():

            team_user.delete()

            view_team.delete()

            try:
                request.cls.view_user.delete()
            except django.db.models.deletion.ProtectedError:
                pass

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

            item_two = getattr(request.cls, 'url_two', None)

            if item_two:

                response_two = client.get(request.cls.url_two)

                request.cls.api_data_two = response_two.data

            else:

                request.cls.api_data_two = {}


        yield

        del request.cls.url_view_kwargs['pk']

        del request.cls.api_data_two




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

        api_data_two = recursearray(self.api_data_two, param_value)

        if param_expected is DoesNotExist:

            assert(
                api_data['key'] not in api_data['obj']
                and api_data_two['key'] not in api_data_two['obj']
            )

        else:

            assert(
                api_data['key'] in api_data['obj']
                or api_data_two['key'] in api_data_two['obj']
            )



    def test_api_field_type(self, recursearray, parameterized, param_key_test_data,
        param_value,
        param_expected
    ):
        """Test for type for API Field"""

        api_data = recursearray(self.api_data, param_value)

        api_data_two = recursearray(self.api_data_two, param_value)

        if param_expected is DoesNotExist:

            assert(
                api_data['key'] not in api_data['obj']
                and api_data_two['key'] not in api_data_two['obj']
            )

        else:

            assert(
                type( api_data['value'] ) is param_expected
                or type( api_data_two.get('value', 'is empty') ) is param_expected
            )



class APIFieldsInheritedCases(
    APIFieldsTestCases
):

    model = None

    parameterized_test_data = {}