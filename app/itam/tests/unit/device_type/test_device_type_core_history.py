
import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.models import Organization

from core.models.history import History
from core.tests.abstract.history_entry import HistoryEntry
from core.tests.abstract.history_entry_parent_model import HistoryEntryParentItem


from itam.models.device import DeviceType



class DeviceTypeHistory(TestCase, HistoryEntry, HistoryEntryParentItem):


    model = DeviceType


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.item_create = self.model.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization
        )


        self.history_create = History.objects.get(
            action = int(History.Actions.ADD),
            item_pk = self.item_create.pk,
            item_class = self.model._meta.model_name,
        )

        self.item_change = self.item_create
        self.item_change.name = 'test_item_' + self.model._meta.model_name + '_changed'
        self.item_change.save()

        self.field_after_expected_value = '{"name": "test_item_' + self.model._meta.model_name + '_changed"}'

        self.history_change = History.objects.get(
            action = int(History.Actions.UPDATE),
            item_pk = self.item_change.pk,
            item_class = self.model._meta.model_name,
        )

        self.item_delete = self.model.objects.create(
            name = 'test_item_delete_' + self.model._meta.model_name,
            organization = self.organization
        )

        self.item_delete.delete()

        self.history_delete = History.objects.filter(
            item_pk = self.item_delete.pk,
            item_class = self.model._meta.model_name,
        )

        self.history_delete_children = History.objects.filter(
            item_parent_pk = self.item_delete.pk,
            item_parent_class = self.model._meta.model_name,
        )
