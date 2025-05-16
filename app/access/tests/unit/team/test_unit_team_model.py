from django.contrib.auth.models import GroupManager
from django.test import TestCase


from access.models.team import Team

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

class ModelTestCases(
    TenancyObjectInheritedCases,
):

    manager = GroupManager

    model = Team

    kwargs_item_create = {
        'name': 'teamone'
    }



class TeamModelTest(
    ModelTestCases,
    TestCase,
):



    def test_model_fields_parameter_not_empty_help_text(self):
        """Test Field called with Parameter

        This is a custom test of a test derived of the samae name. It's required
        as the team model extends the Group model.

        During field creation, paramater `help_text` must not be `None` or empty ('')
        """

        group_mode_fields_to_ignore: list = [
            'id',
            'name',
            'group_ptr_id'
        ]

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            if field.attname in group_mode_fields_to_ignore:

                continue

            print(f'Checking field {field.attname} is not empty')

            if (
                field.help_text is None
                or field.help_text == ''
            ):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_type_verbose_name(self):
        """Test Field called with Parameter

        This is a custom test of a test derived of the samae name. It's required
        as the team model extends the Group model.

        During field creation, paramater `verbose_name` must be of type str
        """

        group_mode_fields_to_ignore: list = [
            'name',
        ]

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            if field.attname in group_mode_fields_to_ignore:

                continue

            print(f'Checking field {field.attname} is of type str')

            if not type(field.verbose_name) is str:

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value
