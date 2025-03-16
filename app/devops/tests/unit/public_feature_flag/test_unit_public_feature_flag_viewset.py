from django.contrib.auth.models import User
from django.test import Client, TestCase

from rest_framework_json_api.metadata import JSONAPIMetadata
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse

from access.models.organization import Organization

from api.tests.abstract.viewsets import ViewSetModel
from api.viewsets.common import PublicReadOnlyViewSet, StaticPageNumbering


from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag
from devops.viewsets.public_feature_flag import ViewSet

from itam.models.software import Software



class ViewsetCommon(
    ViewSetModel,
):

    viewset = ViewSet

    route_name = 'v2:public:devops:_public_api_v2_feature_flag'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization
        3. create super user
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        software = Software.objects.create(
            organization = self.organization,
            name = 'software'
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True,
        )

        self.view_user = User.objects.create_user(username="test_view_user", password="password", is_superuser=True)

        self.kwargs = {
            'organization_id': self.organization.id,
            'software_id': software.id,
        }



class ViewsetList(
    ViewsetCommon,
    TestCase,
):


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        self.http_options_response_list = client.options(url)



    def test_view_common_inheritence(self):
        """Common ViewSet inheritence

        Ensure that the public endpoint inherits from the correct ViewSet
        """

        assert issubclass(self.viewset, PublicReadOnlyViewSet)


    def test_view_attr_permission_classes_value(self):
        """Attribute Test
    
        Attribute `permission_classes` must be metadata class `ReactUIMetadata`
        """
    
        view_set = self.viewset()
    
        assert view_set.permission_classes[0] is IsAuthenticatedOrReadOnly



    def test_view_attr_metadata_class_type(self):
        """Attribute Test
    
        Attribute `metadata_class` must be metadata class `ReactUIMetadata`
        """
    
        view_set = self.viewset()
    
        assert view_set.metadata_class is JSONAPIMetadata


    def test_view_attr_pagination_class_value(self):
        """Attribute Test
    
        Attribute `pagination_class` must be metadata class `StaticPageNumbering`
        """
    
        view_set = self.viewset()
    
        assert view_set.pagination_class is StaticPageNumbering
