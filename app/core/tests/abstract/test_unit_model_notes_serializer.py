import django

from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError

from access.models.tenant import Tenant as Organization

from app.tests.abstract.mock_view import MockView

User = django.contrib.auth.get_user_model()



class ModelNotesSerializerTestCases:
    """ Model Notes Serializer Test Suite

    These test cases are for model notes. This Test Suite mist be included
    in serializer tests for a notes model.

    Actual test class must supply the following:

    - self.item - a created note instance
    - self.note_model - a model instance the note will be made for
    - self.note_model_two - a model instance the note will be made for
    - self.valid_data - Serializer dict containing ALL fields for the model.
    """

    model = None
    """Notes Model to test"""

    model_serializer = None
    """Notes Model Serializer to test"""

    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        self.organization_two = Organization.objects.create(name='test_org_two')

        self.content_type = ContentType.objects.get(
            app_label = str(self.model._meta.app_label).lower(),
            model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
        )

        self.content_type_two = ContentType.objects.get(
            app_label = 'core',
            model = 'modelnotes',
        )

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.user_two = User.objects.create_user(username="test_user_view_two", password="password")



    def test_serializer_valid_data_is_valid(self):
        """Serializer Validation Check

        Ensure that valid data does not throw an exception
        """

        data = self.valid_data.copy()

        mock_view = MockView(
            user = self.user,
            model = self.model
        )

        mock_view.kwargs = {
            'model_id': self.note_model.id
        }

        serializer = self.model_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_valid_data_field_content_type(self):
        """Serializer Validation Check

        Ensure that the `content_type` user is obtained by the request object
        and not the data passed.
        """

        data = self.valid_data.copy()

        mock_view = MockView(
            user = self.user,
            model = self.model
        )

        mock_view.kwargs = {
            'model_id': self.note_model.id
        }

        serializer = self.model_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data
        )

        serializer.is_valid(raise_exception = True)
        serializer.save()

        assert serializer.instance.content_type == self.content_type


    def test_serializer_valid_data_field_model(self):
        """Serializer Validation Check

        Ensure that the `model` user is obtained by the request object
        and not the data passed.
        """

        data = self.valid_data.copy()

        mock_view = MockView(
            user = self.user,
            model = self.model
        )

        mock_view.kwargs = {
            'model_id': self.note_model.id
        }

        serializer = self.model_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data
        )

        serializer.is_valid(raise_exception = True)
        serializer.save()

        assert serializer.instance.model == self.note_model


    def test_serializer_valid_data_field_created_by(self):
        """Serializer Validation Check

        Ensure that the `created_by` user is obtained by the request object
        and not the data passed.
        """

        data = self.valid_data.copy()

        mock_view = MockView(
            user = self.user,
            model = self.model
        )

        mock_view.kwargs = {
            'model_id': self.note_model.id
        }

        serializer = self.model_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data
        )

        serializer.is_valid(raise_exception = True)
        serializer.save()

        assert serializer.instance.created_by == self.user


    def test_serializer_valid_data_field_modified_by(self):
        """Serializer Validation Check

        Ensure that the `modified_by` user is obtained by the request object
        and not the data passed.
        """

        data = self.valid_data.copy()

        mock_view = MockView(
            user = self.user,
            model = self.model
        )

        mock_view.action = 'update'

        mock_view.kwargs = {
            'model_id': self.note_model.id
        }

        serializer = self.model_serializer(
            instance = self.item,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data
        )

        serializer.is_valid(raise_exception = True)
        serializer.save()

        assert serializer.instance.modified_by == self.user


    def test_serializer_valid_data_field_content_partial_update(self):
        """Serializer Validation Check

        Ensure that the `content` is updated when editing.
        """

        data = {
            'content': 'a comment to update for partial update'
        }

        mock_view = MockView(
            user = self.user,
            model = self.model
        )

        mock_view.action = 'partial_update'

        mock_view.kwargs = {
            'model_id': self.note_model.id
        }

        serializer = self.model_serializer(
            instance = self.item,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data,
            partial = True,
        )

        serializer.is_valid(raise_exception = True)
        serializer.save()

        assert serializer.instance.content == data['content']


    def test_serializer_valid_data_field_content_update(self):
        """Serializer Validation Check

        Ensure that the `content` is updated when editing.
        """

        data = self.valid_data.copy()

        mock_view = MockView(
            user = self.user,
            model = self.model
        )

        mock_view.action = 'update'

        mock_view.kwargs = {
            'model_id': self.note_model.id
        }

        serializer = self.model_serializer(
            instance = self.item,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data
        )

        serializer.is_valid(raise_exception = True)
        serializer.save()

        assert serializer.instance.content == data['content']
