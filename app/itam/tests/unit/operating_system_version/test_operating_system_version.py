import pytest
import unittest

from django.test import TestCase

from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel

from config_management.models.groups import ConfigGroups, ConfigGroupSoftware

from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class OperatingSystemVersionModel(
    TestCase,
    TenancyModel,
):

    model = OperatingSystemVersion



    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        organization = Organization.objects.create(name='test_org')


        self.parent_item = OperatingSystem.objects.create(
            organization=organization,
            name = 'os_name'
        )

        self.item = self.model.objects.create(
            name = "12",
            operating_system = self.parent_item,
            organization=organization,
        )
