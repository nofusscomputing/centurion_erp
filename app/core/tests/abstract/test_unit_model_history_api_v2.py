from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client

from rest_framework.relations import Hyperlink

from access.models.organization import Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_fields import APITenancyObject



class BaseModelHistoryAPI(
    APITenancyObject
):
    """Model History Base Test Suite

    Do not include this test suite in your tests, use Primary/Client test
    suites below.

    Args:
        APITenancyObject (_type_): _description_
    """

    model = None
    """The History Model class to be tested"""

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item

        """


        self.organization = Organization.objects.create(name='test_org')

        self.view_user = User.objects.create_user(username="test_user_view", password="password", is_superuser=True)



    @classmethod
    def make_request(self):

        self.url_view_kwargs = {
            'app_label': self.audit_object._meta.app_label,
            'model_name': self.audit_object._meta.model_name,
            'model_id': self.audit_object.id,
            'pk': self.history_entry.pk
        }

        client = Client()
        url = reverse('v2:_api_v2_model_history-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        Test case is a duplicate of a test with the same name.
        This model does not have a `model_notes` field.

        model_notes field must exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        Test case is a duplicate of a test with the same name.
        This model does not have a `model_notes` field.

        model_notes field must be str
        """

        pass



    def test_api_field_exists_modified(self):
        """ Test for existance of API Field

        Test case is a duplicate of a test with the same name.
        This model does not have a `modified` field.

        modified field must exist
        """

        assert 'modified' not in self.api_data


    def test_api_field_type_modified(self):
        """ Test for type for API Field

        Test case is a duplicate of a test with the same name.
        This model does not have a `modified` field.

        modified field must be str
        """

        pass



    def test_api_field_exists_content(self):
        """ Test for existance of API Field

        content field must exist
        """

        assert 'content' in self.api_data


    def test_api_field_type_content(self):
        """ Test for type for API Field

        content field must be str
        """

        assert type(self.api_data['content']) is str



    def test_api_field_exists_before(self):
        """ Test for existance of API Field

        before field must exist
        """

        assert 'before' in self.api_data


    def test_api_field_type_before(self):
        """ Test for type for API Field

        before field must be dict
        """

        assert type(self.api_data['before']) is dict



    def test_api_field_exists_after(self):
        """ Test for existance of API Field

        after field must exist
        """

        assert 'after' in self.api_data


    def test_api_field_type_after(self):
        """ Test for type for API Field

        after field must be dict
        """

        assert type(self.api_data['after']) is dict



    def test_api_field_exists_action(self):
        """ Test for existance of API Field

        action field must exist
        """

        assert 'action' in self.api_data


    def test_api_field_type_action(self):
        """ Test for type for API Field

        action field must be int
        """

        assert type(self.api_data['action']) is int



    def test_api_field_exists_user(self):
        """ Test for existance of API Field

        user field must exist
        """

        assert 'user' in self.api_data


    def test_api_field_type_user(self):
        """ Test for type for API Field

        user field must be int
        """

        assert type(self.api_data['user']) is dict


    def test_api_field_exists_user_id(self):
        """ Test for existance of API Field

        user.id field must exist
        """

        assert 'id' in self.api_data['user']


    def test_api_field_type_user_id(self):
        """ Test for type for API Field

        user.id field must be int
        """

        assert type(self.api_data['user']['id']) is int


    def test_api_field_exists_user_display_name(self):
        """ Test for existance of API Field

        user.display_name field must exist
        """

        assert 'display_name' in self.api_data['user']


    def test_api_field_type_user_display_name(self):
        """ Test for type for API Field

        user.display_name field must be str
        """

        assert type(self.api_data['user']['display_name']) is str


    def test_api_field_exists_user_first_name(self):
        """ Test for existance of API Field

        user.first_name field must exist
        """

        assert 'first_name' in self.api_data['user']


    def test_api_field_type_user_first_name(self):
        """ Test for type for API Field

        user.display_name field must be str
        """

        assert type(self.api_data['user']['first_name']) is str


    def test_api_field_exists_user_last_name(self):
        """ Test for existance of API Field

        user.last_name field must exist
        """

        assert 'last_name' in self.api_data['user']


    def test_api_field_type_user_last_name(self):
        """ Test for type for API Field

        user.last_name field must be str
        """

        assert type(self.api_data['user']['last_name']) is str


    def test_api_field_exists_user_username(self):
        """ Test for existance of API Field

        user.username field must exist
        """

        assert 'username' in self.api_data['user']


    def test_api_field_type_user_username(self):
        """ Test for type for API Field

        user.username field must be str
        """

        assert type(self.api_data['user']['username']) is str


    def test_api_field_exists_user_is_active(self):
        """ Test for existance of API Field

        user.is_active field must exist
        """

        assert 'is_active' in self.api_data['user']


    def test_api_field_type_user_is_active(self):
        """ Test for type for API Field

        user.is_active field must be bool
        """

        assert type(self.api_data['user']['is_active']) is bool


    def test_api_field_exists_user_url(self):
        """ Test for existance of API Field

        user.url field must exist
        """

        assert 'url' in self.api_data['user']


    def test_api_field_type_user_url(self):
        """ Test for type for API Field

        user.url field must be Hyperlink
        """

        assert(
            type(self.api_data['user']['url']) is Hyperlink
            or type(self.api_data['user']['url']) is str
        )


    def test_api_field_exists_urls_notes(self):
        """ Test for existance of API Field

        _urls.notes field must exist
        """

        assert True


    def test_api_field_type_urls_notes(self):
        """ Test for type for API Field

        _urls._self field must be str
        """

        assert True



class PrimaryModelHistoryAPI(
    BaseModelHistoryAPI,
):
    """Primary/Parent History Model test suite
    
    Use this test suite to ttest a history model that is either the parent or
    primary model. i.e. not a child model.


    ## Example of test suite for device history

    ``` py

    @classmethod
    def setUpTestData(self):
        super().setUpTestData()

        self.audit_object = self.audit_model.objects.create(
            organization = self.organization,
            name = 'one',
        )


        self.history_entry = self.model.objects.create(
            organization = self.audit_object.organization,
            action = self.model.Actions.ADD,
            user = self.view_user,
            before = {},
            after = {},
            content_type = ContentType.objects.get(
                app_label = self.audit_object._meta.app_label,
                model = self.audit_object._meta.model_name,
            ),
            model = self.audit_object,
        )


        self.url_view_kwargs = {
            'app_label': self.audit_object._meta.app_label,
            'model_name': self.audit_object._meta.model_name,
            'model_id': self.audit_object.id,
            'pk': self.history_entry.pk
        }

        self.make_request()

    ```
    """

    audit_model = None
    """The Model class the history entry will be created for"""


    def test_api_field_exists_model(self):
        """ Test for existance of API Field

        model field must exist
        """

        assert 'model' in self.api_data


    def test_api_field_type_model(self):
        """ Test for type for API Field

        model field must be dict
        """

        assert type(self.api_data['model']) is dict


    def test_api_field_exists_model_id(self):
        """ Test for existance of API Field

        model.id field must exist
        """

        assert 'id' in self.api_data['model']


    def test_api_field_type_model_id(self):
        """ Test for type for API Field

        model.id field must be int
        """

        assert type(self.api_data['model']['id']) is int


    def test_api_field_exists_model_display_name(self):
        """ Test for existance of API Field

        model.display_name field must exist
        """

        assert 'display_name' in self.api_data['model']


    def test_api_field_type_model_display_name(self):
        """ Test for type for API Field

        model.display_name field must be str
        """

        assert type(self.api_data['model']['display_name']) is str


    # def test_api_field_exists_model_name(self):
    #     """ Test for existance of API Field

    #     model.name field must exist
    #     """

    #     assert 'name' in self.api_data['model']


    # def test_api_field_type_model_name(self):
    #     """ Test for type for API Field

    #     model.name field must be str
    #     """

    #     assert type(self.api_data['model']['name']) is str


    def test_api_field_exists_model_url(self):
        """ Test for existance of API Field

        model.url field must exist
        """

        assert 'url' in self.api_data['model']


    def test_api_field_type_model_url(self):
        """ Test for type for API Field

        model.url field must be Hyperlink
        """

        assert(
            type(self.api_data['model']['url']) is Hyperlink
            or type(self.api_data['model']['url']) is str
        )



class ChildModelHistoryAPI(
    PrimaryModelHistoryAPI,
):
    """Child History Model test suite
    
    Use this test suite to test a history model that is a child model.
    """

    audit_model_child = None
    """The child Model class the history entry will be created for"""



    def test_api_field_exists_child_model(self):
        """ Test for existance of API Field

        child_model field must exist
        """

        assert 'child_model' in self.api_data


    def test_api_field_type_child_model(self):
        """ Test for type for API Field

        child_model field must be int
        """

        assert type(self.api_data['child_model']) is dict


    def test_api_field_exists_child_model_id(self):
        """ Test for existance of API Field

        child_model.id field must exist
        """

        assert 'id' in self.api_data['child_model']


    def test_api_field_type_child_model_id(self):
        """ Test for type for API Field

        child_model.id field must be int
        """

        assert type(self.api_data['child_model']['id']) is int


    def test_api_field_exists_child_model_display_name(self):
        """ Test for existance of API Field

        child_model.display_name field must exist
        """

        assert 'display_name' in self.api_data['child_model']


    def test_api_field_type_child_model_display_name(self):
        """ Test for type for API Field

        child_model.display_name field must be str
        """

        assert type(self.api_data['child_model']['display_name']) is str


    # def test_api_field_exists_child_model_name(self):
    #     """ Test for existance of API Field

    #     child_model.name field must exist
    #     """

    #     assert 'name' in self.api_data['child_model']


    # def test_api_field_type_child_model_name(self):
    #     """ Test for type for API Field

    #     child_model.name field must be str
    #     """

    #     assert type(self.api_data['child_model']['name']) is str


    def test_api_field_exists_child_model_url(self):
        """ Test for existance of API Field

        child_model.url field must exist
        """

        assert 'url' in self.api_data['child_model']


    def test_api_field_type_child_model_url(self):
        """ Test for type for API Field

        child_model.url field must be Hyperlink
        """

        assert (
            type(self.api_data['child_model']['url']) is Hyperlink
            or type(self.api_data['child_model']['url']) is str
        )
