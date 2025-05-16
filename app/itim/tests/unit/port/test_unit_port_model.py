import pytest

from django.test import TestCase

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itim.models.services import Port



class PortModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    kwargs_item_create = {
        'number': 1,
    }

    model = Port


    @pytest.mark.skip(reason = 'to be written')
    def test_field_entry_invalid_port_to_high(self):
        """Test Model Field

        Ensure that a validation error is thrown and that is displays to the user
        """
        pass