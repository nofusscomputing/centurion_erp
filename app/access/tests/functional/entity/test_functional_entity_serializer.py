import django
import pytest

from rest_framework.exceptions import ValidationError

User = django.contrib.auth.get_user_model()



class MockView:

    _has_import: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has import permission.
    """

    _has_purge: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has purge permission.
    """

    _has_triage: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has triage permission.
    """



class EntitySerializerTestCases:


    parameterized_test_data: dict = {
        "model_notes": {
            'will_create': True,
        }
    }

    valid_data: dict = {
        'model_notes': 'model notes field'
    }
    """Valid data used by serializer to create object"""



    @pytest.fixture( scope = 'class')
    def setup_data(self,
        request,
        model,
        django_db_blocker,
        organization_one,
    ):

        with django_db_blocker.unblock():

            request.cls.organization = organization_one

            valid_data = {}

            for base in reversed(request.cls.__mro__):

                if hasattr(base, 'valid_data'):

                    if base.valid_data is None:

                        continue

                    valid_data.update(**base.valid_data)


            if len(valid_data) > 0:

                request.cls.valid_data = valid_data


            if 'organization' not in request.cls.valid_data:

                request.cls.valid_data.update({
                    'organization': request.cls.organization.pk
                })


            request.cls.view_user = User.objects.create_user(username="cafs_test_user_view", password="password")


        yield

        with django_db_blocker.unblock():

            request.cls.view_user.delete()

            del request.cls.valid_data



    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_data,
    ):

        pass


    def test_serializer_valid_data(self, create_serializer):
        """Serializer Validation Check

        Ensure that when creating an object with valid data, no validation
        error occurs.
        """

        view_set = MockView()

        serializer = create_serializer(
            context = {
                'view': view_set,
            },
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_valid_data_missing_field_is_valid(self, parameterized, param_key_test_data,
        create_serializer,
        param_value,
        param_will_create,
    ):
        """Serializer Validation Check

        Ensure that when creating an object with a user with import permission
        and with valid data, no validation error occurs.
        """

        valid_data = self.valid_data.copy()

        del valid_data[param_value]

        view_set = MockView()

        view_set._has_import = True

        serializer = create_serializer(
            context = {
                'view': view_set,
            },
            data = valid_data
        )

        is_valid = serializer.is_valid(raise_exception = False)

        assert (
            (
                not param_will_create
                and param_will_create == is_valid
            )
            or param_will_create == is_valid
        )



class EntitySerializerInheritedCases(
    EntitySerializerTestCases,
):

    parameterized_test_data: dict = None

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""


    def test_serializer_valid_data_missing_field_raises_exception(self, parameterized, param_key_test_data,
        create_serializer,
        param_value,
        param_exception_key,
    ):
        """Serializer Validation Check

        Ensure that when creating an object with a user with import permission
        and with valid data, no validation error occurs.
        """

        valid_data = self.valid_data.copy()

        del valid_data[param_value]

        view_set = MockView()

        with pytest.raises(ValidationError) as err:

            serializer = create_serializer(
                context = {
                    'view': view_set,
                },
                data = valid_data
            )

            is_valid = serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()[param_value][0] == param_exception_key



class EntitySerializerPyTest(
    EntitySerializerTestCases,
):

    parameterized_test_data: dict = None
