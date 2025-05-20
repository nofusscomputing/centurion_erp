import pytest


@pytest.mark.models
class MetaAbstractModelTestCases:
    

    # @pytest.fixture( scope = 'class', autouse = True)
    # def setup_class(cls, model):
    #     
    pass


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
    pass
