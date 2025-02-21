from django.contrib.auth.models import  User

from app.tests.abstract.models import TenancyModel

from access.models.organization import Organization


class ModelNotesModel(
    TenancyModel
):
    """Model Notes Test Suite
    
    These test cases are for unit testing a model notes model. The parent class
    must define the object `self.item`
    """

    model = None
    """Model to be tested"""


    @classmethod
    def setUpTestData(self):
        """Setup Test
        
        Parent class must define `self.item`
        """

        self.organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")



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
                and field.attname != 'modelnotes_ptr_id'
            ):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value
