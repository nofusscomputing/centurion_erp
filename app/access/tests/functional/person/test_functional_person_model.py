import pytest

from access.tests.functional.entity.test_functional_entity_model import (
    EntityModelInheritedCases,
    TicketAssigneeEntityTestCases,
)



@pytest.mark.model_person
class PersonModelTestCases(
    TicketAssigneeEntityTestCases,
    EntityModelInheritedCases,
):
    pass



class PersonModelInheritedCases(
    PersonModelTestCases,
):

    def test_function_linked_model_person__f_name_m_name_l_name_dob(self,
        model_person,
        model, model_kwargs,
    ):
        """Test linking to parent model `person`

        when fields `'f_name', 'm_name', 'l_name', 'dob'` match, link to the model
        """

        if model._meta.pk.related_model is not model_person:
            pytest.xfail( reason = 'model not a child of person. test is N/A.' )


        kwargs = model_kwargs()

        kwargs_person = kwargs.copy()
        del kwargs_person['email']
        del kwargs_person['directory']
        kwargs_person['entity_type'] = 'person'

        person = model_person.objects.create( **kwargs_person )

        obj = model.objects.create( **kwargs )

        assert person.id == obj.id


    def test_function_linked_model_person__f_name_l_name_dob(self,
        model_person,
        model, model_kwargs,
    ):
        """Test linking to parent model `person`

        when fields `'f_name', 'l_name', 'dob'` match, link to the model
        """


        if model._meta.pk.related_model is not model_person:
            pytest.xfail( reason = 'model not a child of person. test is N/A.' )


        kwargs = model_kwargs()

        kwargs_person = kwargs.copy()
        del kwargs_person['email']
        del kwargs_person['directory']
        del kwargs_person['m_name']
        kwargs_person['entity_type'] = 'person'

        person = model_person.objects.create( **kwargs_person )

        obj = model.objects.create( **kwargs )

        assert person.id == obj.id


    def test_function_linked_model_person__f_name_m_name_l_name(self,
        model_person,
        model, model_kwargs,
    ):
        """Test linking to parent model `person`

        when fields `'f_name', 'm_name', 'l_name'` match, link to the model
        """


        if model._meta.pk.related_model is not model_person:
            pytest.xfail( reason = 'model not a child of person. test is N/A.' )


        kwargs = model_kwargs()

        kwargs_person = kwargs.copy()
        del kwargs_person['email']
        del kwargs_person['directory']
        del kwargs_person['dob']
        kwargs_person['entity_type'] = 'person'

        person = model_person.objects.create( **kwargs_person )

        obj = model.objects.create( **kwargs )

        assert person.id == obj.id


    def test_function_linked_model_person__f_name_l_name(self,
        model_person,
        model, model_kwargs,
    ):
        """Test linking to parent model `person`

        when fields `'f_name', 'l_name'` match, link to the model
        """


        if model._meta.pk.related_model is not model_person:
            pytest.xfail( reason = 'model not a child of person. test is N/A.' )


        kwargs = model_kwargs()

        kwargs_person = kwargs.copy()
        del kwargs_person['email']
        del kwargs_person['directory']
        del kwargs_person['dob']
        del kwargs_person['m_name']
        kwargs_person['entity_type'] = 'person'

        person = model_person.objects.create( **kwargs_person )

        obj = model.objects.create( **kwargs )

        assert person.id == obj.id




@pytest.mark.module_access
class PersonModelPyTest(
    PersonModelTestCases,
):
    pass
