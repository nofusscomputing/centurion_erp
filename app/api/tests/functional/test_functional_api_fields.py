import pytest

from django.db import models
from django.test import Client

from rest_framework.relations import Hyperlink


@pytest.mark.functional
class APIFieldsTestCases:
    """ API field Rendering Test Suite

    This test suite tests the rendering of API fieilds.

    ## Additional Items

    You may find a scenario where you are unable to have all fileds available
    within a single request. to overcome this, this test suite has the features
    available wherein you can prepare an additional item for an additional
    check. the following is required before the API request is made:

    - additional item created and stored in attribute `self.item_two`

    This object should be created in fixture `create_model` to which you should
    override to add this object.Once you have these two objects, an additional
    check will be done and each test will check both API requests. If the field
    is found in either api request the test will pass
    """

    @property
    def parameterized_api_fields(self) -> dict:

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



    @pytest.fixture( scope = 'class')
    def create_model(self, request, django_db_blocker,
        model, model_kwargs
    ):

        item = None

        with django_db_blocker.unblock():

            kwargs_many_to_many = {}

            kwargs = {}

            for key, value in model_kwargs.items():

                field = model._meta.get_field(key)

                if isinstance(field, models.ManyToManyField):

                    kwargs_many_to_many.update({
                        key: value
                    })

                else:

                    kwargs.update({
                        key: value
                    })


            item = model.objects.create(
                **kwargs
            )

            for key, value in kwargs_many_to_many.items():

                field = getattr(item, key)

                for entry in value:

                    field.add(entry)

            request.cls.item = item

        yield item

        with django_db_blocker.unblock():

            item.delete()



    @pytest.fixture( scope = 'class')
    def make_request(self,
        request,
        api_request_permissions,
    ):

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )
        response = client.get( self.item.get_url() )

        request.cls.api_data = response.data



        item_two = getattr(request.cls, 'item_two', None)

        if item_two:

            response_two = client.get( self.item_two.get_url() )

            request.cls.api_data_two = response_two.data

        else:

            request.cls.api_data_two = {}


        yield



    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        create_model,
        make_request,
    ):

        pass



    @pytest.mark.regression
    def test_api_field_exists(self, recursearray,
        parameterized, param_key_api_fields,
        param_value,
        param_expected
    ):
        """Test for existance of API Field"""

        api_data = recursearray(self.api_data, param_value)

        api_data_two = recursearray(self.api_data_two, param_value)

        if param_expected is models.NOT_PROVIDED:

            assert(
                api_data['key'] not in api_data['obj']
                and api_data_two['key'] not in api_data_two['obj']
            )

        else:

            assert(
                api_data['key'] in api_data['obj']
                or api_data_two['key'] in api_data_two['obj']
            )



    @pytest.mark.regression
    def test_api_field_type(self, recursearray,
        parameterized, param_key_api_fields,
        param_value,
        param_expected
    ):
        """Test for type for API Field"""

        api_data = recursearray(self.api_data, param_value)

        api_data_two = recursearray(self.api_data_two, param_value)

        if param_expected is models.NOT_PROVIDED:

            assert(
                api_data['key'] not in api_data['obj']
                and api_data_two['key'] not in api_data_two['obj']
            )

        else:

            assert(
                type( api_data.get('value', 'is empty') ) is param_expected
                or type( api_data_two.get('value', 'is empty') ) is param_expected
            )


@pytest.mark.api
class APIFieldsInheritedCases(
    APIFieldsTestCases
):

    pass
