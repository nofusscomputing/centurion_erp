import pytest


@pytest.mark.models
class CenturionAuditModelTestCases:

    # @pytest.fixture( scope = 'class', autouse = True)
    # def setup_class(cls, model):
    #     pass
    pass



class CenturionAuditModelInheritedCases(
    CenturionAuditModelTestCases,
):

    pass



class CenturionAuditModelPyTest(
    CenturionAuditModelTestCases,
):
    pass
