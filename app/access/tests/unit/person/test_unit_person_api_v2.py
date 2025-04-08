from django.test import TestCase

from access.models.person import Person

from access.tests.unit.entity.test_unit_entity_api_v2 import (
    EntityAPIInheritedCases,
)



class APITestCases(
    EntityAPIInheritedCases,
):

    model = Person

    kwargs_item_create: dict = {}

    url_ns_name = '_api_v2_entity_sub'


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create.update({
            'f_name': 'Ian',
            'm_name': 'Peter',
            'l_name': 'Funny',
            'dob': '2025-04-08',
        })

        super().setUpTestData()



    def test_api_field_exists_f_name(self):
        """ Test for existance of API Field

        f_name field must exist
        """

        assert 'f_name' in self.api_data


    def test_api_field_type_f_name(self):
        """ Test for type for API Field

        f_name field must be str
        """

        assert type(self.api_data['f_name']) is str


    def test_api_field_exists_m_name(self):
        """ Test for existance of API Field

        m_name field must exist
        """

        assert 'm_name' in self.api_data


    def test_api_field_type_f_name(self):
        """ Test for type for API Field

        m_name field must be str
        """

        assert type(self.api_data['m_name']) is str


    def test_api_field_exists_l_name(self):
        """ Test for existance of API Field

        l_name field must exist
        """

        assert 'l_name' in self.api_data


    def test_api_field_type_f_name(self):
        """ Test for type for API Field

        l_name field must be str
        """

        assert type(self.api_data['l_name']) is str


    def test_api_field_exists_dob(self):
        """ Test for existance of API Field

        dob field must exist
        """

        assert 'dob' in self.api_data


    def test_api_field_type_dob(self):
        """ Test for type for API Field

        dob field must be str
        """

        assert type(self.api_data['dob']) is str



class PersonAPIInheritedCases(
    APITestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Person
    """

    kwargs_item_create: dict = None

    model = None


class PersonAPITest(
    APITestCases,
    TestCase,
):

    pass
