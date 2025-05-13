import django
import re

from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest
import requests

from access.models.organization import Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from app.tests.abstract.model_permissions import ModelPermissions

from project_management.models.projects import Project
from project_management.models.project_milestone import ProjectMilestone

from core.models.ticket.ticket import Ticket, RelatedTickets, TicketCategory
from core.models.ticket.ticket_comment import TicketComment

from core.tests.unit.ticket_depreciated.ticket_permission.field_based_permissions import ITSMTicketFieldBasedPermissions, ProjectTicketFieldBasedPermissions

from settings.models.user_settings import UserSettings

User = django.contrib.auth.get_user_model()



class SetUp:

    ticket_type:str = None

    ticket_type_enum: int = None

    model = Ticket

    # app_namespace = 'Assistance'

    # url_name_view = '_ticket_request_view'

    # url_name_add = '_ticket_request_add'

    # url_name_change = '_ticket_request_change'

    # url_name_delete = '_ticket_request_delete'

    # url_delete_response = reverse('Assistance:Requests')

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a manufacturer
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        user_settings = UserSettings.objects.get(user = self.add_user)
        user_settings.default_organization = self.organization
        user_settings.save()

        self.category = TicketCategory.objects.create(
            organization = organization,
            name = 'a category'
        )

        self.category_two = TicketCategory.objects.create(
            organization = organization,
            name = 'a category_two'
        )


        self.item = self.model.objects.create(
            organization=organization,
            title = 'A ' + self.ticket_type + ' ticket',
            description = 'the ticket body',
            ticket_type = self.ticket_type_enum,
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.second_item = self.model.objects.create(
            organization=organization,
            title = 'A second ' + self.ticket_type + ' ticket',
            description = 'the ticket body of item two',
            ticket_type = self.ticket_type_enum,
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.third_item = self.model.objects.create(
            organization=organization,
            title = 'A third ' + self.ticket_type + ' ticket',
            description = 'the ticket body of item two',
            ticket_type = self.ticket_type_enum,
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.project = Project.objects.create(
            name = 'ticket permissions project name',
            organization = organization
        )

        self.project_two = Project.objects.create(
            name = 'ticket permissions project name two',
            organization = organization
        )


        self.url_view_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.url_add_kwargs = {'ticket_type': self.ticket_type}

        self.add_data = {
            'title': 'an add ticket',
            'organization': self.organization.id,
        }

        self.url_change_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.change_data = {'title': 'an change to ticket'}

        self.url_delete_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.delete_data = {'title': 'a delete to ticket'}


        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])


        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        change_team.permissions.set([change_permissions])

        self.change_team = change_team



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        delete_team = Team.objects.create(
            team_name = 'delete_team',
            organization = organization,
        )

        delete_team.permissions.set([delete_permissions])


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )

        # Import user/permissions

        import_permissions = Permission.objects.get(
                codename = 'import_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        import_team = Team.objects.create(
            team_name = 'import_team',
            organization = organization,
        )

        import_team.permissions.set([change_permissions, import_permissions])


        self.import_user = User.objects.create_user(username="test_user_import", password="password")
        teamuser = TeamUsers.objects.create(
            team = import_team,
            user = self.import_user
        )

        # Triage user/permissions

        triage_permissions = Permission.objects.get(
                codename = 'triage_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        triage_team = Team.objects.create(
            team_name = 'triage_team',
            organization = organization,
        )

        triage_team.permissions.set([change_permissions, triage_permissions])


        self.triage_user = User.objects.create_user(username="test_user_triage", password="password")
        teamuser = TeamUsers.objects.create(
            team = triage_team,
            user = self.triage_user
        )




class ActionComments(SetUp):

    def test_ticket_action_comment_assign_user_added_status_change(self):
        """Action Comment test
        Confirm a 'status changed' action comment is created when a user is added as assigned
        """

        self.item.assigned_users.add(self.add_user.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"changed status to assigned", str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_assign_user_added_user_assigned(self):
        """Action Comment test
        Confirm a 'user assigned' action comment is created when a user is added as assigned
        """

        self.item.assigned_users.add(self.add_user.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"assigned @" + self.add_user.username , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_assign_user_added_status_update(self):
        """Action Comment test
        When a user is assigned and the status is 'new', the ticket status must update
        to 'assigned'
        """

        self.item.assigned_users.add(self.add_user.id)

        assert self.item.status == Ticket.TicketStatus.All.ASSIGNED


    def test_ticket_action_comment_assign_user_removed_status_change(self):
        """Action Comment test
        Confirm a 'status changed' action comment is created when a user is removed as assigned
        """

        self.item.assigned_users.add(self.add_user.id)

        self.item.assigned_users.remove(self.add_user.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"changed status to new", str(comment.body).lower()):

                action_comment = True

        assert action_comment


    # @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_assign_user_removed_user_unassigned(self):
        """Action Comment test
        Confirm a 'user unassigned' action comment is created when a user is removed as assigned
        """

        self.item.assigned_users.add(self.add_user.id)

        self.item.assigned_users.remove(self.add_user.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"unassigned @" + self.add_user.username, str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_assign_user_remove_status_update(self):
        """Action Comment test
        When a user is unassigned and the status is 'assigned', the ticket status must update
        to 'new'
        """

        self.item.assigned_users.add(self.add_user.id)

        self.item.assigned_users.remove(self.add_user.id)

        assert self.item.status == Ticket.TicketStatus.All.NEW


    def test_ticket_action_comment_assign_team_added_status_change(self):
        """Action Comment test
        Confirm a 'status changed' action comment is created when a user is added as assigned
        """

        self.item.assigned_teams.add(self.change_team.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"changed status to assigned", str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_assign_team_added_team_assigned(self):
        """Action Comment test
        Confirm a 'team assigned' action comment is created when a team is added as assigned
        """

        self.item.assigned_teams.add(self.change_team.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"assigned team @" + self.change_team.team_name , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_assign_team_added_status_update(self):
        """Action Comment test
        When a team is assigned and the status is 'new', the ticket status must update
        to 'assigned'
        """

        self.item.assigned_teams.add(self.change_team.id)

        assert self.item.status == Ticket.TicketStatus.All.ASSIGNED


    def test_ticket_action_comment_assign_team_remove_status_change(self):
        """Action Comment test
        Confirm a 'status changed' action comment is created when a user is removed as assigned
        """

        self.item.assigned_teams.add(self.change_team.id)

        self.item.assigned_teams.remove(self.change_team.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"changed status to new", str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_assign_team_remove_team_assigned(self):
        """Action Comment test
        Confirm a 'team assigned' action comment is created when a team is removed as assigned
        """

        self.item.assigned_teams.add(self.change_team.id)

        self.item.assigned_teams.remove(self.change_team.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"unassigned team @" + self.change_team.team_name , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_assign_team_remove_status_update(self):
        """Action Comment test
        When a team is unassigned and the status is 'assigned', the ticket status must update
        to 'new'
        """

        self.item.assigned_teams.add(self.change_team.id)

        self.item.assigned_teams.remove(self.change_team.id)

        assert self.item.status == Ticket.TicketStatus.All.NEW



    def test_ticket_action_comment_category_added(self):
        """Action Comment test
        Confirm an' action comment is created when a `category` is added
        """

        self.item.category = self.category

        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"changed category from none to \$ticket_category-" + str(self.category.id) , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_category_remove(self):
        """Action Comment test
        Confirm an action comment is created when the `category` is removed
        """

        self.item.category = self.category

        self.item.save()

        self.item.category = None

        self.item.save()


        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"changed category from \$ticket_category-" + str(self.category.id) + " to none", str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_category_change(self):
        """Action Comment test
        Confirm an action comment is created when a `category` is changed
        """

        self.item.category = self.category

        self.item.save()


        self.item.category = self.category_two

        self.item.save()


        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"changed category from \$ticket_category-" + str(self.category.id) + r" to \$ticket_category-" + str(self.category_two.id) , str(comment.body).lower()):

                action_comment = True

        assert action_comment



    def test_ticket_action_comment_parent_ticket_added(self):
        """Action Comment test
        Confirm an' action comment is created when a `parent_ticket` is added
        """

        self.item.parent_ticket = self.second_item

        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"parent ticket changed from none to #" + str(self.second_item.id) , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_parent_ticket_remove(self):
        """Action Comment test
        Confirm an action comment is created when the `category` is removed
        """

        self.item.parent_ticket = self.second_item

        self.item.save()

        self.item.parent_ticket = None

        self.item.save()


        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"parent ticket changed from #" + str(self.second_item.id) + " to none", str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_parent_ticket_change(self):
        """Action Comment test
        Confirm an action comment is created when a `category` is changed
        """

        self.item.parent_ticket = self.second_item

        self.item.save()


        self.item.parent_ticket = self.third_item

        self.item.save()


        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"parent ticket changed from #" + str(self.second_item.id) + r" to #" + str(self.third_item.id) , str(comment.body).lower()):

                action_comment = True

        assert action_comment



    def test_ticket_action_comment_subscribed_users_added_user_subscribed(self):
        """Action Comment test
        Confirm a 'user subscribed' action comment is created when a user is added as subscribed
        """

        self.item.subscribed_users.add(self.add_user.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"added @" + self.add_user.username + " as watching" , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_subscribed_users_removed_user_unsubscribed(self):
        """Action Comment test
        Confirm a 'user unsubscribed' action comment is created when a user is removed as subscribed
        """

        self.item.subscribed_users.add(self.add_user.id)
        self.item.subscribed_users.remove(self.add_user.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"removed @" + self.add_user.username + " as watching" , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_subscribed_teams_added_team_subscribed(self):
        """Action Comment test
        Confirm a 'team subscribed' action comment is created when a team is added as subscribed
        """

        self.item.subscribed_teams.add(self.change_team.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"added team @" + self.change_team.team_name + " as watching" , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_subscribed_teams_removed_team_unsubscribed(self):
        """Action Comment test
        Confirm a 'team unsubscribed' action comment is created when a team is removed as subscribed
        """

        self.item.subscribed_teams.add(self.change_team.id)
        self.item.subscribed_teams.remove(self.change_team.id)

        comments = TicketComment.objects.filter(
            ticket=self.item.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        for comment in comments:

            if re.match(r"removed team @" + self.change_team.team_name + " as watching" , str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_related_ticket_added_type_related_source(self):
        """Action Comment test
        Confirm an 'related' action comment is created for the source ticket
        when a ticket is added with type 'related'.
        """

        from_ticket = self.item
        to_ticket = self.second_item


        related_ticket = RelatedTickets.objects.create(
            from_ticket_id = from_ticket,
            to_ticket_id = to_ticket,
            how_related = RelatedTickets.Related.RELATED,
            organization=self.organization,
        )

        comments = TicketComment.objects.filter(
            ticket=from_ticket.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'added #{from_ticket.id} as related to #{to_ticket.id}'

        for comment in comments:

            if re.match(comment_body, str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_related_ticket_added_type_related_destination(self):
        """Action Comment test
        Confirm an 'related' action comment is created for the destination ticket
        when a ticket is added with type 'related'.
        """

        from_ticket = self.item
        to_ticket = self.second_item

        related_ticket = RelatedTickets.objects.create(
            from_ticket_id = from_ticket,
            to_ticket_id = to_ticket,
            how_related = RelatedTickets.Related.RELATED,
            organization=self.organization,
        )

        comments = TicketComment.objects.filter(
            ticket=to_ticket.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'added #{to_ticket.id} as related to #{from_ticket.id}'

        for comment in comments:

            if re.match(comment_body, str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_related_ticket_added_type_blocks_source(self):
        """Action Comment test
        Confirm a 'related' action comment is created for the source ticket
        when a ticket is added with type 'blocks'.
        """

        from_ticket = self.item
        to_ticket = self.second_item


        related_ticket = RelatedTickets.objects.create(
            from_ticket_id = from_ticket,
            to_ticket_id = to_ticket,
            how_related = RelatedTickets.Related.BLOCKS,
            organization=self.organization,
        )

        comments = TicketComment.objects.filter(
            ticket=from_ticket.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'added #{from_ticket.id} as blocking #{to_ticket.id}'

        for comment in comments:

            if re.match(comment_body, str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_related_ticket_added_type_blocks_destination(self):
        """Action Comment test
        Confirm an 'related' action comment is created for the destination ticket
        when a ticket is added with type 'blocks'.
        """

        from_ticket = self.item
        to_ticket = self.second_item

        related_ticket = RelatedTickets.objects.create(
            from_ticket_id = from_ticket,
            to_ticket_id = to_ticket,
            how_related = RelatedTickets.Related.BLOCKS,
            organization=self.organization,
        )

        comments = TicketComment.objects.filter(
            ticket=to_ticket.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'added #{to_ticket.id} as blocked by #{from_ticket.id}'

        for comment in comments:

            if re.match(comment_body, str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_related_ticket_added_type_blocked_by_source(self):
        """Action Comment test
        Confirm a 'related' action comment is created for the source ticket
        when a ticket is added with type 'blocked_by'.
        """

        from_ticket = self.item
        to_ticket = self.second_item


        related_ticket = RelatedTickets.objects.create(
            from_ticket_id = from_ticket,
            to_ticket_id = to_ticket,
            how_related = RelatedTickets.Related.BLOCKED_BY,
            organization=self.organization,
        )

        comments = TicketComment.objects.filter(
            ticket=from_ticket.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'added #{from_ticket.id} as blocked by #{to_ticket.id}'

        for comment in comments:

            if re.match(comment_body, str(comment.body).lower()):

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_related_ticket_added_type_blocked_by_destination(self):
        """Action Comment test
        Confirm an 'related' action comment is created for the destination ticket
        when a ticket is added with type 'blocked_by'.
        """

        from_ticket = self.item
        to_ticket = self.second_item

        related_ticket = RelatedTickets.objects.create(
            from_ticket_id = from_ticket,
            to_ticket_id = to_ticket,
            how_related = RelatedTickets.Related.BLOCKED_BY,
            organization=self.organization,
        )

        comments = TicketComment.objects.filter(
            ticket=to_ticket.pk,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'added #{to_ticket.id} as blocking #{from_ticket.id}'

        for comment in comments:

            if re.match(comment_body, str(comment.body).lower()):

                action_comment = True

        assert action_comment


    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_related_ticket_removed(self):
        """Action Comment test
        Confirm an action comment is created when a related ticket is removed
        """

        pass



    def test_ticket_action_comment_project_added(self):
        """Action Comment test
        Confirm a 'project added' action comment is created for the ticket
        when a project is added
        """

        from_ticket = self.item
        to_ticket = self.second_item

        # prepare
        self.item.project = None
        self.item.save()

        # create fresh project as id will be unique for test 
        project = Project.objects.create(
            organization = self.item.organization,
            name = 'ticket_project_add'
        )

        # add project
        self.item.project = project
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed project from None to $project-{project.id}'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_project_removed(self):
        """Action Comment test
        Confirm a 'project added' action comment is created for the ticket
        when a project is added
        """

        from_ticket = self.item
        to_ticket = self.second_item

        # create fresh project as id will be unique for test 
        project = Project.objects.create(
            organization = self.item.organization,
            name = 'ticket_project_remove'
        )

        # prepare
        self.item.project = project
        self.item.save()

        # remove project
        self.item.project = None
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed project from $project-{project.id} to None'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_project_changed(self):
        """Action Comment test
        Confirm a 'project added' action comment is created for the ticket
        when a project is added
        """

        from_ticket = self.item
        to_ticket = self.second_item

        # create fresh project as id will be unique for test 
        project = Project.objects.create(
            organization = self.item.organization,
            name = 'ticket_project_change'
        )

        project_two = Project.objects.create(
            organization = self.item.organization,
            name = 'ticket_project_change_two'
        )

        # prepare
        self.item.project = project
        self.item.save()

        # remove project
        self.item.project = project_two
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed project from $project-{project.id} to $project-{project_two.id}'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment



    def test_ticket_action_comment_milestone_added(self):
        """Action Comment test
        Confirm a 'project added' action comment is created for the ticket
        when a project is added
        """

        from_ticket = self.item
        to_ticket = self.second_item

        # create fresh project as id will be unique for test 
        project = Project.objects.create(
            organization = self.item.organization,
            name = 'ticket_project_milestone_add'
        )

        milestone = ProjectMilestone.objects.create(
            organization = self.item.organization,
            name = 'ticket_milestone_add',
            project = project
        )

        # prepare
        self.item.project = project
        self.item.save()

        # add milestone
        self.item.milestone = milestone
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed milestone from None to $milestone-{milestone.id}'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_milestone_removed(self):
        """Action Comment test
        Confirm a 'project added' action comment is created for the ticket
        when a project is added
        """

        from_ticket = self.item
        to_ticket = self.second_item

        # create fresh project as id will be unique for test 
        project = Project.objects.create(
            organization = self.item.organization,
            name = 'ticket_project_milestone_remove'
        )

        milestone = ProjectMilestone.objects.create(
            organization = self.item.organization,
            name = 'ticket_milestone_remove',
            project = project
        )

        # prepare
        self.item.project = project
        self.item.milestone = milestone
        self.item.save()

        # remove milestone
        self.item.milestone = None
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed milestone from $milestone-{milestone.id} to None'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_milestone_changed(self):
        """Action Comment test
        Confirm a 'project added' action comment is created for the ticket
        when a project is added
        """

        from_ticket = self.item
        to_ticket = self.second_item

        # create fresh project as id will be unique for test 
        project = Project.objects.create(
            organization = self.item.organization,
            name = 'ticket_project_milestone_change'
        )

        
        milestone = ProjectMilestone.objects.create(
            organization = self.item.organization,
            name = 'ticket_milestone_change',
            project = project
        )


        milestone_two = ProjectMilestone.objects.create(
            organization = self.item.organization,
            name = 'ticket_milestone_change_two',
            project = project
        )


        # prepare
        self.item.project = project
        self.item.milestone = milestone
        self.item.save()

        # change milestone
        self.item.milestone = milestone_two
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed milestone from $milestone-{milestone.id} to $milestone-{milestone_two.id}'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment



    def test_ticket_action_comment_planned_start_date_added(self):
        """Action Comment test
        
        When the field `planned_start_date` has a value added it must create
        an action comment
        """

        from_value = None
        to_value = '2025-01-27 00:01:00+00:00'

        # prepare
        self.item.planned_start_date = from_value
        self.item.save()

        # add desired value
        self.item.planned_start_date = datetime.strptime(to_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Planned Start Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_planned_start_date_change(self):
        """Action Comment test
        
        When the field `planned_start_date` has a value change it must create
        an action comment
        """

        from_value = '2025-01-27 00:02:00+00:00'
        to_value = '2025-01-27 00:03:00+00:00'

        # prepare
        self.item.planned_start_date = datetime.strptime(from_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        # add desired value
        self.item.planned_start_date = datetime.strptime(to_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Planned Start Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_planned_start_date_remove(self):
        """Action Comment test
        
        When the field `planned_start_date` has a value removed it must create
        an action comment
        """

        from_value = '2025-01-27 00:02:00+00:00'
        to_value = None

        # prepare
        self.item.planned_start_date = datetime.strptime(from_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        # add desired value
        self.item.planned_start_date = None
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Planned Start Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment



    def test_ticket_action_comment_planned_finish_date_added(self):
        """Action Comment test
        
        When the field `planned_finish_date` has a value added it must create
        an action comment
        """

        from_value = None
        to_value = '2025-01-27 01:01:00+00:00'

        # prepare
        self.item.planned_finish_date = from_value
        self.item.save()

        # add desired value
        self.item.planned_finish_date = datetime.strptime(to_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Planned Finish Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_planned_finish_date_change(self):
        """Action Comment test
        
        When the field `planned_finish_date` has a value change it must create
        an action comment
        """

        from_value = '2025-01-27 01:02:00+00:00'
        to_value = '2025-01-27 01:03:00+00:00'

        # prepare
        self.item.planned_finish_date = datetime.strptime(from_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        # add desired value
        self.item.planned_finish_date = datetime.strptime(to_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Planned Finish Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_planned_finish_date_remove(self):
        """Action Comment test
        
        When the field `planned_finish_date` has a value removed it must create
        an action comment
        """

        from_value = '2025-01-27 01:04:00+00:00'
        to_value = None

        # prepare
        self.item.planned_finish_date = datetime.strptime(from_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        # add desired value
        self.item.planned_finish_date = None
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Planned Finish Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment



    def test_ticket_action_comment_real_start_date_added(self):
        """Action Comment test
        
        When the field `real_start_date` has a value added it must create
        an action comment
        """

        from_value = None
        to_value = '2025-01-27 00:01:00+00:00'

        # prepare
        self.item.real_start_date = from_value
        self.item.save()

        # add desired value
        self.item.real_start_date = datetime.strptime(to_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Real Start Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_real_start_date_change(self):
        """Action Comment test
        
        When the field `real_start_date` has a value change it must create
        an action comment
        """

        from_value = '2025-01-27 00:02:00+00:00'
        to_value = '2025-01-27 00:03:00+00:00'

        # prepare
        self.item.real_start_date = datetime.strptime(from_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        # add desired value
        self.item.real_start_date = datetime.strptime(to_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Real Start Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_real_start_date_remove(self):
        """Action Comment test
        
        When the field `real_start_date` has a value removed it must create
        an action comment
        """

        from_value = '2025-01-27 00:02:00+00:00'
        to_value = None

        # prepare
        self.item.real_start_date = datetime.strptime(from_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        # add desired value
        self.item.real_start_date = None
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Real Start Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment



    def test_ticket_action_comment_real_finish_date_added(self):
        """Action Comment test
        
        When the field `real_finish_date` has a value added it must create
        an action comment
        """

        from_value = None
        to_value = '2025-01-27 01:01:00+00:00'

        # prepare
        self.item.real_finish_date = from_value
        self.item.save()

        # add desired value
        self.item.real_finish_date = datetime.strptime(to_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Real Finish Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_real_finish_date_change(self):
        """Action Comment test
        
        When the field `real_finish_date` has a value change it must create
        an action comment
        """

        from_value = '2025-01-27 01:02:00+00:00'
        to_value = '2025-01-27 01:03:00+00:00'

        # prepare
        self.item.real_finish_date = datetime.strptime(from_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        # add desired value
        self.item.real_finish_date = datetime.strptime(to_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Real Finish Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment


    def test_ticket_action_comment_real_finish_date_remove(self):
        """Action Comment test
        
        When the field `real_finish_date` has a value removed it must create
        an action comment
        """

        from_value = '2025-01-27 01:04:00+00:00'
        to_value = None

        # prepare
        self.item.real_finish_date = datetime.strptime(from_value, '%Y-%m-%d %H:%M:%S%z')
        self.item.save()

        # add desired value
        self.item.real_finish_date = None
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False

        comment_body: str = f'changed Real Finish Date from _{from_value}_ to **{to_value}**'

        for comment in comments:

            if str(comment_body).lower() == str(comment.body).lower():

                action_comment = True

        assert action_comment



    def test_ticket_action_comment_description_change(self):
        """Action Comment test
        
        When the field `real_finish_date` has a value removed it must create
        an action comment
        """

        from_value = 'description text'
        to_value = 'description text\n\nadditional text'

        # prepare
        self.item.description = from_value
        self.item.save()

        # add desired value
        self.item.description = to_value
        self.item.save()

        comments = TicketComment.objects.filter(
            ticket=self.item,
            comment_type = TicketComment.CommentType.ACTION
        )

        action_comment: bool = False


        for comment in comments:

            if '+additional text' in str(comment.body):

                action_comment = True

        assert action_comment



class TicketPermissions(
    SetUp,
    ModelPermissions,
):


    @pytest.mark.skip(reason="To be written")
    def test_permission_purge(self):

        pass



class ITSMTicketPermissions(
    TicketPermissions,
    ITSMTicketFieldBasedPermissions,
):

    pass



class ProjectTicketPermissions(
    TicketPermissions,
    ProjectTicketFieldBasedPermissions,
):

    pass



class ChangeTicketPermissions(ITSMTicketPermissions, TestCase):

    ticket_type = 'change'

    ticket_type_enum: int = int(Ticket.TicketType.CHANGE.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_change_view'

    url_name_add = '_ticket_change_add'

    url_name_change = '_ticket_change_change'

    url_name_delete = '_ticket_change_delete'

    url_delete_response = reverse('ITIM:Changes')



class IncidentTicketPermissions(ITSMTicketPermissions, TestCase):

    ticket_type = 'incident'

    ticket_type_enum: int = int(Ticket.TicketType.INCIDENT.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_incident_view'

    url_name_add = '_ticket_incident_add'

    url_name_change = '_ticket_incident_change'

    url_name_delete = '_ticket_incident_delete'

    url_delete_response = reverse('ITIM:Incidents')



class ProblemTicketPermissions(ITSMTicketPermissions, TestCase):

    ticket_type = 'problem'

    ticket_type_enum: int = int(Ticket.TicketType.PROBLEM.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_problem_view'

    url_name_add = '_ticket_problem_add'

    url_name_change = '_ticket_problem_change'

    url_name_delete = '_ticket_problem_delete'

    url_delete_response = reverse('ITIM:Problems')



class ProjectTaskPermissions(ProjectTicketPermissions, TestCase):

    ticket_type = 'project_task'

    ticket_type_enum: int = int(Ticket.TicketType.PROJECT_TASK.value)

    app_namespace = 'Project Management'

    url_name_view = '_project_task_view'

    url_name_add = '_project_task_add'

    url_name_change = '_project_task_change'

    url_name_delete = '_project_task_delete'




    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a manufacturer
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        super().setUpTestData()

        self.item = self.model.objects.create(
            organization = self.organization,
            title = 'Amended ' + self.ticket_type + ' ticket',
            description = 'the ticket body',
            ticket_type = int(Ticket.TicketType.REQUEST.value),
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value),
            project = self.project
        )

        self.url_add_kwargs = {'project_id': self.project.id, 'ticket_type': self.ticket_type}

        self.url_change_kwargs = {'project_id': self.project.id, 'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.url_delete_kwargs = {'project_id': self.project.id, 'ticket_type': self.ticket_type, 'pk': self.project.id}

        # self.url_delete_kwargs = {'pk': self.project.id}

        self.url_view_kwargs = {'project_id': self.project.id, 'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.url_delete_response = reverse('Project Management:_project_view', kwargs={'pk': self.project.id})



class RequestTicketPermissions(ITSMTicketPermissions, TestCase):

    ticket_type = 'request'

    ticket_type_enum: int = int(Ticket.TicketType.REQUEST.value)

    app_namespace = 'Assistance'

    url_name_view = '_ticket_request_view'

    url_name_add = '_ticket_request_add'

    url_name_change = '_ticket_request_change'

    url_name_delete = '_ticket_request_delete'

    url_delete_response = reverse('Assistance:Requests')





class ChangeTicketActionComments(ActionComments, TestCase):

    ticket_type = 'change'

    ticket_type_enum: int = int(Ticket.TicketType.CHANGE.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_change_view'

    url_name_add = '_ticket_change_add'

    url_name_change = '_ticket_change_change'

    url_name_delete = '_ticket_change_delete'

    url_delete_response = reverse('ITIM:Changes')



class IncidentTicketActionComments(ActionComments, TestCase):

    ticket_type = 'incident'

    ticket_type_enum: int = int(Ticket.TicketType.INCIDENT.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_incident_view'

    url_name_add = '_ticket_incident_add'

    url_name_change = '_ticket_incident_change'

    url_name_delete = '_ticket_incident_delete'

    url_delete_response = reverse('ITIM:Incidents')



class ProblemTicketActionComments(ActionComments, TestCase):

    ticket_type = 'problem'

    ticket_type_enum: int = int(Ticket.TicketType.PROBLEM.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_problem_view'

    url_name_add = '_ticket_problem_add'

    url_name_change = '_ticket_problem_change'

    url_name_delete = '_ticket_problem_delete'

    url_delete_response = reverse('ITIM:Problems')



class ProjectTaskActionComments(ActionComments, TestCase):

    ticket_type = 'project_task'

    ticket_type_enum: int = int(Ticket.TicketType.PROJECT_TASK.value)

    app_namespace = 'Project Management'

    url_name_view = '_project_task_view'

    url_name_add = '_project_task_add'

    url_name_change = '_project_task_change'

    url_name_delete = '_project_task_delete'




    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a manufacturer
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        super().setUpTestData()

        self.item = self.model.objects.create(
            organization = self.organization,
            title = 'Amended ' + self.ticket_type + ' ticket',
            description = 'the ticket body',
            ticket_type = int(Ticket.TicketType.REQUEST.value),
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value),
            project = self.project
        )

        self.url_add_kwargs = {'project_id': self.project.id, 'ticket_type': self.ticket_type}

        self.url_change_kwargs = {'project_id': self.project.id, 'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.url_delete_kwargs = {'project_id': self.project.id, 'ticket_type': self.ticket_type, 'pk': self.project.id}

        # self.url_delete_kwargs = {'pk': self.project.id}

        self.url_view_kwargs = {'project_id': self.project.id, 'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.url_delete_response = reverse('Project Management:_project_view', kwargs={'pk': self.project.id})



class RequestTicketActionComments(ActionComments, TestCase):

    ticket_type = 'request'

    ticket_type_enum: int = int(Ticket.TicketType.REQUEST.value)

    app_namespace = 'Assistance'

    url_name_view = '_ticket_request_view'

    url_name_add = '_ticket_request_add'

    url_name_change = '_ticket_request_change'

    url_name_delete = '_ticket_request_delete'

    url_delete_response = reverse('Assistance:Requests')



