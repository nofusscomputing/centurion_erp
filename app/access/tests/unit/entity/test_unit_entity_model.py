from django.test import TestCase

from access.models.entity import Entity

from app.tests.unit.test_unit_models import TenancyObjectInheritedCases



class EntityModelTestCases(
    TenancyObjectInheritedCases,
):

    model = Entity

    kwargs_item_create: dict = {}


    def test_attribute_type_history_app_label(self):
        """Attribute Type

        history_app_name is of type str
        """

        assert type(self.model.history_app_label) is str


    def test_attribute_value_history_app_label(self):
        """Attribute Type

        history_app_name is of type str
        """

        assert self.model.history_app_label == 'access'




    def test_attribute_type_history_model_name(self):
        """Attribute Type

        history_model_name is of type str
        """

        assert type(self.model.history_model_name) is str


    def test_attribute_value_history_model_name(self):
        """Attribute Type

        history_model_name is of type str
        """

        assert self.model.history_model_name == 'entity'



    def test_attribute_type_kb_model_name(self):
        """Attribute Type

        kb_model_name is of type str
        """

        assert type(self.model.kb_model_name) is str


    def test_attribute_value_kb_model_name(self):
        """Attribute Type

        kb_model_name is of type str
        """

        assert self.model.kb_model_name == 'entity'



    def test_attribute_type_note_basename(self):
        """Attribute Type

        note_basename is of type str
        """

        assert type(self.model.note_basename) is str


    def test_attribute_value_note_basename(self):
        """Attribute Type

        note_basename is of type str
        """

        assert self.model.note_basename == '_api_v2_entity_note'



class EntityModelInheritedCases(
    EntityModelTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Entity
    """

    kwargs_item_create: dict = None

    model = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create.update(
            super().kwargs_item_create
        )

        super().setUpTestData()



class EntityModelTest(
    EntityModelTestCases,
    TestCase,
):

    pass
