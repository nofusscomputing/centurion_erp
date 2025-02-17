
# import pytest
# import unittest
# import requests

# from django.test import TestCase, Client

# from access.models import Organization

# from core.models.history import History
# from core.tests.abstract.history_entry import HistoryEntry
# from core.tests.abstract.history_entry_child_model import HistoryEntryChildItem

# from access.models import Team

# from django.contrib.auth.models import Group


# class TeamHistory(TestCase, HistoryEntry, HistoryEntryChildItem):


#     model = Team


#     @classmethod
#     def setUpTestData(self):
#         """ Setup Test """

#         organization = Organization.objects.create(name='test_org')

#         self.organization = organization

#         self.item_parent = organization

#         self.item_create = self.model.objects.create(
#             team_name = 'test_item_' + self.model._meta.model_name,
#             organization = self.organization
#         )


#         self.history_create = History.objects.get(
#             action = int(History.Actions.ADD),
#             item_pk = self.item_create.pk,
#             item_class = self.model._meta.model_name,
#         )

#         self.item_change = self.item_create
#         self.item_change.team_name = 'test_item_' + self.model._meta.model_name + '_changed'
#         self.item_change.save()

#         self.field_after_expected_value = '{"name": "test_org_' + self.item_change.team_name + '", "team_name": "' + self.item_change.team_name + '"}'

#         self.history_change = History.objects.get(
#             action = int(History.Actions.UPDATE),
#             item_pk = self.item_change.pk,
#             item_class = self.model._meta.model_name,
#         )

#         debug = Group.objects.all()

#         self.item_delete = self.model.objects.create(
#             team_name = 'test_item_delete_' + self.model._meta.model_name,
#             organization = self.organization
#         )

#         self.deleted_pk = self.item_delete.pk

#         self.item_delete.delete()

#         self.history_delete = History.objects.get(
#             action = int(History.Actions.DELETE),
#             item_pk = self.deleted_pk,
#             item_class = self.model._meta.model_name,
#         )

#         self.history_delete_children = History.objects.filter(
#             item_parent_pk = self.deleted_pk,
#             item_parent_class = self.item_parent._meta.model_name,
#         )
