import pytest


@pytest.mark.models
class CenturionAbstractModelTestCases:

    @pytest.fixture( scope = 'class', autouse = True)
    def setup_class(cls, model):
        pass



class CenturionAbstractModelInheritedCases(
    CenturionAbstractModelTestCases,
):

    pass



class CenturionAbstractModelPyTest(
    CenturionAbstractModelTestCases,
):
    pass
