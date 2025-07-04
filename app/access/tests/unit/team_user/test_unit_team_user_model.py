import django
from django.test import TestCase

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from centurion.tests.unit.test_unit_models import NonTenancyObjectInheritedCases

User = django.contrib.auth.get_user_model()



class TeamUsersModel(
    NonTenancyObjectInheritedCases,
    TestCase,
):

    model = TeamUsers



    @classmethod
    def setUpTestData(self):
        """ Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        self.parent_item = Team.objects.create(
            team_name = 'test_team',
            organization = self.organization,
        )

        team_user = User.objects.create_user(username="test_self.team_user", password="password")

        self.kwargs_item_create = {
            'team': self.parent_item,
            'user': team_user
        }

        super().setUpTestData()



    def test_model_has_property_parent_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert hasattr(self.model, 'parent_object')


    def test_model_property_parent_object_returns_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert self.item.parent_object == self.parent_item

