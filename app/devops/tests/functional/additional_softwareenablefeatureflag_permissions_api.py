import pytest



class AdditionalTestCases:


    def test_returned_data_from_user_and_global_organizations_only(
        self
    ):
        """Check items returned

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        pytest.xfail( reason = 'model does not use global org' )
