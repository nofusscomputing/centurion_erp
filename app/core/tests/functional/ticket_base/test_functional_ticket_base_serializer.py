from django.contrib.auth.models import User
from django.test import TestCase

from access.models.organization import Organization

from core.serializers.ticket import (
    TicketBase,
    ModelSerializer
)

from project_management.models.project_milestone import (
    Project,
    ProjectMilestone,
)



class SerializerTestCases:

    model = TicketBase
    """Model to test"""

    create_model_serializer = ModelSerializer
    """Serializer to test"""

    valid_data: dict = {
        "display_name": "tester ticket",
        "organization": None,
        "external_system": TicketBase.Ticket_ExternalSystem.CUSTOM_1,
        "external_ref": 1,
        "parent_ticket": None,
        "ticket_type": "request",
        "status": TicketBase.TicketStatus.NEW,
        "category": None,
        "title": "title2",
        "description": "the description",
        "project": None,
        "milestone": None,
        "urgency": TicketBase.TicketUrgency.LOW,
        "impact": TicketBase.TicketImpact.LOW,
        "priority": TicketBase.TicketPriority.LOW,
        "priority_badge": None,
        "opened_by": None,
        "subscribed_to": [],
        "assigned_to": [],
        "planned_start_date": '2025-04-29T00:00:00Z',
        "planned_finish_date": '2025-04-29T01:00:00Z',
        "real_start_date": '2025-04-29T00:02:00Z',
        "real_finish_date": '2025-04-29T00:03:00Z',
        "tto": 0,
        "ttr": 0,
        "is_deleted": False,
        "is_solved": False,
        "date_solved": None,
        "is_closed": False,
        "date_closed": None,
    }
    """Valid data used by serializer to create object"""


    @classmethod
    def setUpTestData(self):
        """Setup Test"""
        
        self.organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.project_one = Project.objects.create(
            organization = self.organization,
            name = 'proj 1'
        )

        self.milestone_one = ProjectMilestone.objects.create(
            organization = self.organization,
            name = 'milestone one',
            project = self.project_one
        )

        self.milestone_two = ProjectMilestone.objects.create(
            organization = self.organization,
            name = 'milestone two',
            project = self.project_one
        )


        self.project_two = Project.objects.create(
            organization = self.organization,
            name = 'proj 2'
        )

        self.milestone_three = ProjectMilestone.objects.create(
            organization = self.organization,
            name = 'milestone three',
            project = self.project_two
        )

        self.valid_data.update({
            'organization': self.organization.pk,
            'opened_by': self.user.pk,
            'project': self.project_one.pk,
            'milestone': self.milestone_one.pk,
        })




    def test_serializer_valid_data(self):
        """Serializer Validation Check

        Ensure that when creating an object with valid data, no validation
        error occurs.
        """

        serializer = self.create_model_serializer(
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)



class TicketBaseSerializerInheritedCases(
    SerializerTestCases,
):

    create_model_serializer = None
    """Serializer to test"""

    model = None
    """Model to test"""

    valid_data: dict = {}
    """Valid data used by serializer to create object"""


    @classmethod
    def setUpTestData(self):

        self.valid_data = {
            **super().valid_data,
            **self.valid_data
        }

        super().setUpTestData()



class TicketBaseSerializerTest(
    SerializerTestCases,
    TestCase,
):

    pass
