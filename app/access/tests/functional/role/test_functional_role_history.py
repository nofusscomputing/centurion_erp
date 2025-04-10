from django.test import TestCase

from access.models.role_history import Role, RoleHistory

from core.tests.abstract.test_functional_history import HistoryEntriesCommon



class HistoryTestCases(
    HistoryEntriesCommon,
):

    history_model = RoleHistory

    kwargs_create_obj: dict = {}

    kwargs_delete_obj: dict = {}

    model = Role


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



class RoleHistoryTest(
    HistoryTestCases,
    TestCase,
):

    kwargs_create_obj: dict = {
        'name': 'original_name'
    }

    kwargs_delete_obj: dict = {
        'name': 'delete obj'
    }
