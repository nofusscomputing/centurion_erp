import pytest
import unittest
import requests

from django.test import TestCase

from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel

from itam.models.software import Software, SoftwareVersion



class SoftwareVersionModel(
    TestCase,
    TenancyModel
):

    model = SoftwareVersion


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.software = Software.objects.create(
            organization=organization,
            name = 'deviceone'
        )

        self.item = self.model.objects.create(
            organization=organization,
            name = '12',
            software = self.software
        )
