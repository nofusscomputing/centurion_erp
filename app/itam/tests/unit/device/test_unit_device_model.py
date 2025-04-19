from django.test import TestCase

import pytest


from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.device import Device


class DeviceModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = Device


    @pytest.mark.skip(reason="to be written")
    def test_device_move_organization(user):
        """Move Organization test

        When a device moves organization, devicesoftware and devicesoftware table data
        must also move organizations
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_software_action(user):
        """Ensure only software that is from the same organization or is global can be added to the device
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_not_global(user):
        """Devices are not global items.

            Ensure that a device can't be set to be global.
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_operating_system_version_only_one(user):
        """model deviceoperatingsystem must only contain one value per device
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_device_model_same_organization(user):
        """ Can only add a device model from same organization """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_device_model_global(user):
        """ Can add a device model that is set is_global=true """
        pass
