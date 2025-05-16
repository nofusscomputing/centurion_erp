import pytest

from django.db import models

from access.models.entity import Entity

from centurion.tests.unit.test_unit_models import (
    PyTestTenancyObjectInheritedCases,
)



class EntityModelTestCases(
    PyTestTenancyObjectInheritedCases,
):

    base_model = Entity

    kwargs_create_item: dict = {}

    sub_model_type = 'entity'
    """Sub Model Type
    
    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """


    parameterized_fields: dict = {
        "entity_type": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': False,
            # 'field_parameter_default_value': 'entity',
            'field_parameter_verbose_name_type': str
        },
        # "asset_number": {
        #     'field_type': models.fields.CharField,
        #     'field_parameter_default_exists': False,
        #     'field_parameter_verbose_name_type': str,
        # },
        # "serial_number": {
        #     'field_type': models.fields.CharField,
        #     'field_parameter_default_exists': False,
        #     'field_parameter_verbose_name_type': str,
        # }
    }



    @pytest.fixture( scope = 'class')
    def setup_model(self,
        request,
        model,
        django_db_blocker,
        organization_one,
        organization_two
    ):

        with django_db_blocker.unblock():

            request.cls.organization = organization_one

            request.cls.different_organization = organization_two

            kwargs_create_item = {}

            for base in reversed(request.cls.__mro__):

                if hasattr(base, 'kwargs_create_item'):

                    if base.kwargs_create_item is None:

                        continue

                    kwargs_create_item.update(**base.kwargs_create_item)


            if len(kwargs_create_item) > 0:

                request.cls.kwargs_create_item = kwargs_create_item


            if 'organization' not in request.cls.kwargs_create_item:

                request.cls.kwargs_create_item.update({
                    'organization': request.cls.organization
                })

        yield



    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_model,
        create_model,
    ):

        pass



    def test_class_inherits_entity(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, Entity)


    def test_attribute_type_history_app_label(self):
        """Attribute Type

        history_app_label is of type str
        """

        assert type(self.model.history_app_label) is str


    def test_attribute_value_history_app_label(self):
        """Attribute Type

        history_app_label has been set, override this test case with the value
        of attribute `history_app_label`
        """

        assert self.model.history_app_label == 'access'



    def test_attribute_type_history_model_name(self):
        """Attribute Type

        history_model_name is of type str
        """

        assert type(self.model.history_model_name) is str


    def test_attribute_value_history_model_name(self):
        """Attribute Type

        history_model_name has been set, override this test case with the value
        of attribute `history_model_name`
        """

        assert self.model.history_model_name == 'entity'



    def test_attribute_type_kb_model_name(self):
        """Attribute Type

        kb_model_name is of type str
        """

        assert type(self.model.kb_model_name) is str


    def test_attribute_value_kb_model_name(self):
        """Attribute Type

        kb_model_name has been set, override this test case with the value
        of attribute `kb_model_name`
        """

        assert self.model.kb_model_name == 'entity'



    def test_attribute_type_note_basename(self):
        """Attribute Type

        note_basename is of type str
        """

        assert type(self.model.note_basename) is str


    def test_attribute_value_note_basename(self):
        """Attribute Type

        note_basename has been set, override this test case with the value
        of attribute `note_basename`
        """

        assert self.model.note_basename == '_api_v2_entity_note'








    # def test_function_is_property_get_model_type(self):
    #     """Function test

    #     Confirm function `get_model_type` is a property
    #     """

    #     assert type(self.model.get_model_type) is property


    # def test_function_value_get_model_type(self):
    #     """Function test

    #     Confirm function `get_model_type` does not have a value of None
    #     value should be equaul to Meta.sub_model_type
    #     """

    #     assert self.item.get_model_type == self.item._meta.sub_model_type




    def test_function_value_get_related_model(self):
        """Function test

        Confirm function `get_related_model` is of the sub-model type
        """

        assert type(self.item.get_related_model()) == self.model


    def test_function_value_get_url(self):

        assert self.item.get_url() == '/api/v2/access/entity/' + str(self.item.id)



class EntityModelInheritedCases(
    EntityModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model Entity
    """

    kwargs_create_item: dict = {}

    model = None


    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """


    # def test_function_value_get_model_type(self):
    #     """Function test

    #     Confirm function `get_model_type` does not have a value of None
    #     value should be equaul to Meta.sub_model_type
    #     """

    #     assert self.item.get_model_type == self.item._meta.sub_model_type



class EntityModelPyTest(
    EntityModelTestCases,
):


    def test_function_value_get_related_model(self):
        """Function test

        Confirm function `get_related_model` is None for base model
        """

        assert self.item.get_related_model() is None
