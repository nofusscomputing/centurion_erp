from django.db.models.fields import NOT_PROVIDED
from django.test import TestCase

from access.models.person import Person
from access.tests.unit.entity.test_unit_entity_model import (
    EntityModelInheritedCases
)



class ModelTestCases(
    EntityModelInheritedCases,
):

    model = Person

    kwargs_item_create: dict = None



    def test_model_field_dob_optional(self):
        """Test Field

        Field `dob` must be an optional field
        """

        assert self.model._meta.get_field('dob').blank


    def test_model_field_f_name_mandatory(self):
        """Test Field

        Field `f_name` must be a mandatory field
        """

        assert(
            not (
                self.model._meta.get_field('f_name').blank
                and self.model._meta.get_field('f_name').null
            )
            and self.model._meta.get_field('f_name').default is NOT_PROVIDED
        )


    def test_model_field_l_name_mandatory(self):
        """Test Field

        Field `l_name` must be a mandatory field
        """

        assert (
            not (
                self.model._meta.get_field('l_name').blank
                and self.model._meta.get_field('l_name').null
            )
            and self.model._meta.get_field('l_name').default is NOT_PROVIDED
        )



class PersonModelInheritedCases(
    ModelTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Person
    """

    kwargs_item_create: dict = None

    model = None



class PersonModelTest(
    ModelTestCases,
    TestCase,
):

    # model = Person

    kwargs_item_create: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }
