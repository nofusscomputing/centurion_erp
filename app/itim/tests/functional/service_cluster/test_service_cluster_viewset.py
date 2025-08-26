import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from itim.models.clusters import Cluster
from itim.models.services import Service, Port



@pytest.mark.model_cluster
class ViewSetBase(
    MetadataAttributesFunctional,
):

    model = Service

    app_namespace = 'v2'

    url_name = '_api_v2_service_cluster'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        super().presetUpTestData()

        super().setUpTestData()


        cluster = Cluster.objects.create(
            organization=self.organization,
            name = 'cluster'
        )

        port = Port.objects.create(
            organization=self.organization,
            number = 80,
            protocol = Port.Protocol.TCP
        )

        self.item = self.model.objects.create(
            organization=self.organization,
            name = 'os name',
            cluster = cluster,
            config_key_variable = 'value'
        )

        self.other_org_item = self.model.objects.create(
            organization=self.different_organization,
            name = 'os name b',
            cluster = cluster,
            config_key_variable = 'values'
        )

        self.item.port.set([ port ])



        self.url_view_kwargs = {'cluster_id': cluster.id, 'pk': self.item.id}

        self.url_kwargs = {'cluster_id': cluster.id}


@pytest.mark.module_itim
class ServiceMetadata(
    ViewSetBase,
    TestCase
):

    pass
