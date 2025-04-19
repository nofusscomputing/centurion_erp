from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from django.test import TestCase

from assistance.models.knowledge_base import KnowledgeBaseCategory



class KnowledgeBaseModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = KnowledgeBaseCategory
