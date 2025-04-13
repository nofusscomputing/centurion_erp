from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from settings.models.external_link import ExternalLink



class ExternalLinkTests(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = ExternalLink
