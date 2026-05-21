
from django.test import TestCase



class ViewSetAttributesUnit:
    """ Unit Tests For View Set attributes.

    These tests ensure that View sets contian the required attributesthat are
    used by the API .
    """


    def test_attribute_exists_layout(self):
        """Attrribute Test, Exists

        Ensure attribute `layout` exists
        """

        pass


    def test_attribute_type_layout(self):
        """Attrribute Test, Type

        Ensure attribute `layout` is of type `list`
        """

        pass


    def test_attribute_not_callable_layout(self):
        """Attrribute Test, Not Callable

        Attribute must be a property

        Ensure attribute `layout` is not callable.
        """

        pass

# other tests required
# - filterset_fields
# - metadata_class
# - search_fields
# - documentation
# - model_documentation or is in `model.documentation`
