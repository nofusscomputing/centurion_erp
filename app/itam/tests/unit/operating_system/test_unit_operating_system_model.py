from django.test import TestCase

import pytest

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.operating_system import OperatingSystem



class OperatingSystemModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = OperatingSystem


    @pytest.mark.skip(reason="to be written")
    def test_operating_system_update_is_global_no_change(user):
        """Once operating_system is set to global it can't be changed.

            global status can't be changed as non-global items may reference the item.
        """

        pass

    @pytest.mark.skip(reason="to be written")
    def test_operating_system_prevent_delete_if_used(user):
        """Any operating_system in use by a operating_system must not be deleted.

            i.e. A global os can't be deleted
        """

        pass


    @pytest.mark.skip(reason="to be written")
    def test_operating_system_version_installs_by_os_count(user):
        """Operating System Versions has a count field that must be accurate

            The count is of model OperatingSystemVersion linked to model operating_systemOperatingSystem
        """

        pass
