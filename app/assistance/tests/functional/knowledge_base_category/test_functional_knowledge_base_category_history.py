from django.test import TestCase

from assistance.models.knowledge_base_category_history import KnowledgeBaseCategory, KnowledgeBaseCategoryHistory

from core.tests.abstract.test_functional_history import HistoryEntriesCommon



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = KnowledgeBaseCategory

    history_model = KnowledgeBaseCategoryHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.obj = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_original
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_delete
        )

        self.call_the_banners()
