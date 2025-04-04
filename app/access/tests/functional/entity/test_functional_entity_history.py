from django.test import TestCase

from access.models.entity_history import Entity, EntityHistory

from core.tests.abstract.test_functional_history import HistoryEntriesCommon



class HistoryTestCases(
    HistoryEntriesCommon,
):

    field_name = 'model_notes'

    history_model = EntityHistory

    kwargs_create_obj: dict = {}

    kwargs_delete_obj: dict = {}

    model = None


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.obj = self.model.objects.create(
            organization = self.organization,
            model_notes = self.field_value_original,
            **self.kwargs_create_obj,
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            model_notes = 'another note',
            **self.kwargs_delete_obj,
        )

        self.call_the_banners()



class EntityHistoryInheritedCases(
    HistoryTestCases,
):

    model = None
    """Entity model to test"""



class EntityHistoryTest(
    HistoryTestCases,
    TestCase,
):

    model = Entity
