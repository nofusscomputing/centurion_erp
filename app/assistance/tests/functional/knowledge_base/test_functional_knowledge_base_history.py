from django.contrib.auth.models import User
from django.test import TestCase

from assistance.models.knowledge_base_history import KnowledgeBase, KnowledgeBaseHistory

from core.tests.abstract.test_functional_history import HistoryEntriesCommon



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = KnowledgeBase

    history_model = KnowledgeBaseHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.field_name = 'title'

        user = User.objects.create_user(username="test_user_view", password="password")

        self.obj = self.model.objects.create(
            organization = self.organization,
            title = self.field_value_original,
            content = 'sadsadsa',
            responsible_user = user,
            target_user = user,
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            title = self.field_value_delete,
            content = 'sadsadsa',
            responsible_user = user,
            target_user = user,
        )

        self.call_the_banners()
