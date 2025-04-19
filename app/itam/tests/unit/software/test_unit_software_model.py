import pytest

from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.software import Software



class SoftwareModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = Software



    @pytest.mark.skip(reason="to be written")
    def test_software_must_have_organization(self):
        """ Software must have organization set """
        pass

    @pytest.mark.skip(reason="to be written")
    def test_software_update_is_global_no_change(self):
        """Once software is set to global it can't be changed.

            global status can't be changed as non-global items may reference the item.
        """

        pass

    @pytest.mark.skip(reason="to be written")
    def test_software_prevent_delete_if_used(self):
        """Any software in use by a software must not be deleted.

            i.e. A software has an action set for the software.
        """

        pass
