import pytest

from django.db.models import fields

from rest_framework.exceptions import ValidationError

from access.models.organization import Organization
from access.tests.unit.tenancy_object.test_unit_tenancy_object import (
    TenancyObjectInheritedCases as AccessTenancyObjectInheritedCases
)

from core.tests.unit.mixin.test_unit_history_save import (
    SaveHistory,
    SaveHistoryMixinInheritedCases
)



class ModelMetaTestCases:



    def test_attribute_exists_ordering(self):
        """Test for existance of field in `<model>.Meta`

        Attribute `ordering` must be defined in `Meta` class.
        """

        assert 'ordering' in self.model._meta.original_attrs


    def test_attribute_not_empty_ordering(self):
        """Test field `<model>.Meta` is not empty

        Attribute `ordering` must contain values
        """

        assert (
            self.model._meta.original_attrs['ordering'] is not None
            and len(list(self.model._meta.original_attrs['ordering'])) > 0
        )


    def test_attribute_type_ordering(self):
        """Test field `<model>.Meta` is not empty

        Attribute `ordering` must be of type list.
        """

        assert type(self.model._meta.original_attrs['ordering']) is list



    def test_field_exists_verbose_name(self):
        """Test for existance of field in `<model>.Meta`

        Attribute `verbose_name` must be defined in `Meta` class.
        """

        assert 'verbose_name' in self.model._meta.original_attrs


    def test_field_type_verbose_name(self):
        """Test field `<model>.Meta` is not empty

        Attribute `verbose_name` must be of type str.
        """

        assert type(self.model._meta.original_attrs['verbose_name']) is str



    def test_field_exists_verbose_name_plural(self):
        """Test for existance of field in `<model>.Meta`

        Attribute `verbose_name_plural` must be defined in `Meta` class.
        """

        assert 'verbose_name_plural' in self.model._meta.original_attrs


    def test_field_type_verbose_name_plural(self):
        """Test field `<model>.Meta` is not empty

        Attribute `verbose_name_plural` must be of type str.
        """

        assert type(self.model._meta.original_attrs['verbose_name_plural']) is str



class ModelFieldsTestCases:



    @pytest.mark.skip( reason = 'see test __doc__' )
    def test_model_fields_parameter_mandatory_has_no_default(self):
        """Test Field called with Parameter

        ## Test skipped

        fields dont have enough info to determine if mandatory, so this item can't be 
        tested.

        Some fields can be set as `null=false` with `blank=false` however `default=<value>`
        ensures it's populated with a desired default.

        If a field is set as null=false, there must not be a default parameter
        """

        fields_have_test_value: bool = True

        fields_to_skip_checking: list = [
            'created',
            'is_global',
            'modified'
        ]

        for field in self.model._meta.fields:

            if field.attname not in fields_to_skip_checking:

                print(f'Checking field {field.attname} to see if mandatory')

                if not getattr(field, 'null', True) and not getattr(field, 'blank', True):

                    if getattr(field, 'default', fields.NOT_PROVIDED) != fields.NOT_PROVIDED:

                        print(f'    Failure on field {field.attname}')

                        fields_have_test_value = False


        assert fields_have_test_value



    def test_model_fields_parameter_has_help_text(self):
        """Test Field called with Parameter

        During field creation, it should have been called with paramater `help_text`
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} has attribute "help_text"')

            if not hasattr(field, 'help_text'):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_type_help_text(self):
        """Test Field called with Parameter

        During field creation, paramater `help_text` must be of type str
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} is of type str')

            if not type(field.help_text) is str:

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_not_empty_help_text(self):
        """Test Field called with Parameter

        During field creation, paramater `help_text` must not be `None` or empty ('')
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} is not empty')

            if (
                (
                    field.help_text is None
                    or field.help_text == ''
                )
                and not str(field.attname).endswith('_ptr_id')
            ):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value



    def test_model_fields_parameter_has_verbose_name(self):
        """Test Field called with Parameter

        During field creation, it should have been called with paramater `verbose_name`
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} has attribute "verbose_name"')

            if not hasattr(field, 'verbose_name'):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_type_verbose_name(self):
        """Test Field called with Parameter

        During field creation, paramater `verbose_name` must be of type str
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} is of type str')

            if not type(field.verbose_name) is str:

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_not_empty_verbose_name(self):
        """Test Field called with Parameter

        During field creation, paramater `verbose_name` must not be `None` or empty ('')
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} is not empty')

            if (
                field.verbose_name is None
                or field.verbose_name == ''
            ):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value




class Models(
    ModelFieldsTestCases,
    ModelMetaTestCases,
):
    """Test Cases for All defined models"""

    pass



class TenancyObjectInheritedCases(
    Models,
    AccessTenancyObjectInheritedCases
):
    """Test Cases for models that inherit from

    access.models.tenancy.TenancyObject"""

    model = None


    kwargs_item_create: dict = {
        'name': 'one'
    }


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        self.different_organization = Organization.objects.create(name='test_different_organization')

        self.kwargs_item_create.update({
            'organization': self.organization,
            'model_notes': 'notes',
        })

        self.item = self.model.objects.create(
            **self.kwargs_item_create,
        )



    def test_create_validation_exception_no_organization(self):
        """ Tenancy objects must have an organization

        Must not be able to create an item without an organization
        """

        kwargs_item_create = self.kwargs_item_create.copy()

        del kwargs_item_create['organization']

        with pytest.raises(ValidationError) as err:

            self.model.objects.create(
                **kwargs_item_create,
            )

        assert err.value.get_codes()['organization'] == 'required'




class NonTenancyObjectInheritedCases(
    Models,
    SaveHistoryMixinInheritedCases,
):
    """Test Cases for models that don't inherit from

    access.models.tenancy.TenancyObject"""

    model = None

    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.item = self.model.objects.create(
            **self.kwargs_item_create,
        )



    def test_class_inherits_save_history(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, SaveHistory)
