from django.db.models.fields import NOT_PROVIDED
from django.test import TestCase

from access.models.contact import Contact
from access.tests.unit.person.test_unit_person_model import (
    Person,
    PersonModelInheritedCases
)



class ModelTestCases(
    PersonModelInheritedCases,
):

    model = Contact

    kwargs_item_create: dict = {
        'email': 'ipweird@unit.test',
    }



    def test_model_field_directory_optional(self):
        """Test Field

        Field `dob` must be an optional field
        """

        assert self.model._meta.get_field('directory').blank


    def test_model_field_directory_optional_default(self):
        """Test Field

        Field `directory` default value is `True`
        """

        assert (
            self.model._meta.get_field('directory').default is True
            and self.model._meta.get_field('directory').null is False
        )


    def test_model_field_email_mandatory(self):
        """Test Field

        Field `email` must be a mandatory field
        """

        assert(
            not (
                self.model._meta.get_field('email').blank
                and self.model._meta.get_field('email').null
            )
            and self.model._meta.get_field('email').default is NOT_PROVIDED
        )


    def test_model_inherits_person(self):
        """Test model inheritence

        model must inherit from Entity sub-model `Person`
        """

        assert issubclass(self.model, Person)




class ContactModelInheritedCases(
    ModelTestCases,
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



class ContactModelTest(
    ModelTestCases,
    TestCase,
):

    pass
