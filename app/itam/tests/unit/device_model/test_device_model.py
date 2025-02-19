import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel

from itam.models.device_models import DeviceModel



class DeviceModelModel(
    TestCase,
    TenancyModel
):

    model = DeviceModel


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

        self.item = self.model.objects.create(
            organization=organization,
            name = 'device model'
        )


    @pytest.mark.skip(reason="to be written")
    def test_device_model_software_action(user):
        """Ensure only software that is from the same organization or is global can be added to the device
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_model_must_have_organization(user):
        """ Device Model must have organization set """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_model_not_global(user):
        """Devices are not global items.

            Ensure that a device can't be set to be global.
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_model_operating_system_version_only_one(user):
        """model deviceoperatingsystem must only contain one value per device
        """
        pass
