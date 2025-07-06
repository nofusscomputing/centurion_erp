import pytest



class AdditionalTestCases:


    exclude_permission_no_add = [
        ('different_organization_user_forbidden',
            'Permission not restricted to orgs, they are app wide'),
        ]


    exclude_permission_no_change = [
            ('different_organization_user_forbidden',
            'Permission not restricted to orgs, they are app wide'),
        ]


    exclude_permission_no_view = [
        ('different_organization_user_forbidden',
            'Permission not restricted to orgs, they are app wide'),
    ]


    def test_permission_add(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        pytest.xfail( reason = 'Model does not support adding' )



    def test_returned_results_only_user_orgs(self):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        pytest.xfail( reason = 'model is not org based' )


    def test_returned_data_from_user_and_global_organizations_only(
        self
    ):
        """Check items returned

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        pytest.xfail( reason = 'model is not org based' )
