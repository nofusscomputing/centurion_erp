import pytest


@pytest.mark.models
class CenturionSubAbstractModelTestCases:

    # @pytest.fixture( scope = 'class', autouse = True)
    # def setup_class(cls, model):
    #     pass
    pass



class CenturionSubAbstractModelInheritedCases(
    CenturionSubAbstractModelTestCases,
):

    pass



class CenturionSubAbstractModelPyTest(
    CenturionSubAbstractModelTestCases,
):
    pass
