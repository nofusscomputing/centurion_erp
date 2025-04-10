from django.test import TestCase

from access.models.contact import Contact

from access.tests.unit.person.test_unit_person_api_v2 import (
    PersonAPIInheritedCases,
)



class APITestCases(
    PersonAPIInheritedCases,
):

    model = Contact

    kwargs_item_create: dict = {
        'email': 'ipfunny@unit.test',
    }

    url_ns_name = '_api_v2_entity_sub'


    def test_api_field_exists_email(self):
        """ Test for existance of API Field

        email field must exist
        """

        assert 'email' in self.api_data


    def test_api_field_type_email(self):
        """ Test for type for API Field

        email field must be str
        """

        assert type(self.api_data['email']) is str


    def test_api_field_exists_directory(self):
        """ Test for existance of API Field

        directory field must exist
        """

        assert 'directory' in self.api_data


    def test_api_field_type_directory(self):
        """ Test for type for API Field

        directory field must be bool
        """

        assert type(self.api_data['directory']) is bool



class ContactAPIInheritedCases(
    APITestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Contact
    """

    kwargs_item_create: dict = None

    model = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create.update(
            super().kwargs_item_create
        )

        super().setUpTestData()



class ContactAPITest(
    APITestCases,
    TestCase,
):

    pass
