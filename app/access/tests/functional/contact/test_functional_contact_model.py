import pytest

from access.tests.functional.person.test_functional_person_model import PersonModelInheritedCases



@pytest.mark.model_contact
class ContactModelTestCases(
    PersonModelInheritedCases
):
    pass


class ContactModelInheritedCases(
    ContactModelTestCases,
):

    def test_function_linked_model_contact__email(self,
        model_contact,
        model, model_kwargs,
    ):
        """Test linking to parent model `contact`

        when fields `'email'` match, link to the model
        """

        if model._meta.pk.related_model is not model_contact:
            pytest.xfail( reason = 'model not a child of contact. test is N/A.' )


        kwargs = model_kwargs()

        kwargs_contact = kwargs.copy()
        del kwargs_contact['employee_number']
        del kwargs_contact['user']

        contact = model_contact.objects.create( **kwargs_contact )

        obj = model.objects.create( **kwargs )

        assert contact.id == obj.id




@pytest.mark.module_access
class ContactModelPyTest(
    ContactModelTestCases,
):
    pass
