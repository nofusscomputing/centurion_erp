from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from assistance.models.knowledge_base import KnowledgeBase



class KnowledgeBaseModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    kwargs_item_create = {
        'title': 'one',
        'content': 'dict({"key": "one", "existing": "dont_over_write"})'
    }

    model = KnowledgeBase
