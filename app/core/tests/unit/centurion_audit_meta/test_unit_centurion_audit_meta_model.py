import pytest

from core.tests.unit.centurion_sub_abstract.test_unit_centurion_sub_abstract_model import (
    CenturionSubAbstractModelInheritedCases,
)
from core.tests.unit.centurion_audit.test_unit_centurion_audit_model import (
    CenturionAuditModelInheritedCases,
)



@pytest.mark.models
class MetaAbstractModelTestCases(
    CenturionSubAbstractModelInheritedCases,
    CenturionAuditModelInheritedCases
):
    pass
    # parameterized_class_attributes = {
    #     '_audit_enabled': {
    #         'value': False,
    #     },
    #     '_notes_enabled': {
    #         'value': False,
    #     }
    # }



    # check models with model._audit_enabled=True have a model created

    # check models with model._audit_enabled=False DONT have a model created

    # check the Meta class has the correct attributes


    # confirm it exists in sys.modules

    # check they inherit form audithistory parent class



class MetaAbstractModelInheritedCases(
    MetaAbstractModelTestCases,
):

    pass



class MetaAbstractModelPyTest(
    MetaAbstractModelTestCases,
):

    def test_model_is_abstract(self, model):

        assert model._meta.abstract

    def test_model_not_proxy(self, model):

        assert not model._meta.proxy


    def test_model_creation(self):
        """
        This test is a duplicate of a test with the same name. As this model
        is an abstract model this test is not required.
        """
        pass
