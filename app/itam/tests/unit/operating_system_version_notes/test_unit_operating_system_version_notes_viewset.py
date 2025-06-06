from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from itam.models.operating_system import OperatingSystem
from itam.viewsets.operating_system_version_notes import ViewSet



class OperatingSystemVersionNotesViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_operating_system_version_note'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create object that is to be tested against
        2. add kwargs
        3. make list request
        """


        super().setUpTestData()

        self.note_model = self.viewset.model.model.field.related_model.objects.create(
            organization = self.organization,
            name = '11',
            operating_system = OperatingSystem.objects.create(
                organization = self.organization,
                name = 'note model',
            )
        )

        self.kwargs = {
            'operating_system_id': self.note_model.operating_system.pk,
            'model_id': self.note_model.pk,
        }


        client = Client()

        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)
