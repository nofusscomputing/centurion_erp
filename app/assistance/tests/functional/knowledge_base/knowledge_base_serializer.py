import django
import json
import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models.tenant import Tenant as Organization
from access.models.team import Team

from centurion.tests.abstract.mock_view import MockView

from assistance.models.knowledge_base import KnowledgeBase
from assistance.serializers.knowledge_base import KnowledgeBaseModelSerializer

User = django.contrib.auth.get_user_model()



class KnowledgeBaseValidationAPI(
    TestCase,
):

    model = KnowledgeBase

    app_namespace = 'API'
    
    url_name = '_api_knowledgebase'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create a team
        4. Add user to add team
        """

        organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.mock_view = MockView( user = self.user )

        self.organization = organization

        self.add_team = Team.objects.create(
            organization=organization,
            team_name = 'teamone',
            model_notes = 'random note'
        )

        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        self.item_has_target_user = self.model.objects.create(
            organization=organization,
            title = 'random title',
            content = 'random note',
            summary = 'a summary',
            target_user = self.add_user,
            release_date = '2024-01-01 12:00:00',
            expiry_date = '2024-01-01 12:00:01',
            responsible_user = self.add_user,
        )

        self.item_has_target_team = self.model.objects.create(
            organization=organization,
            title = 'random title',
            content = 'random note',
            summary = 'a summary',
            release_date = '2024-01-01 12:00:00',
            expiry_date = '2024-01-01 12:00:01',
            responsible_user = self.add_user,
        )

        self.item_has_target_team.target_team.set([ self.add_team ])
