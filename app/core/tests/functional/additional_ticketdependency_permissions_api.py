import pytest



class AdditionalTestCases:


    permission_no_add = [
            ('anon_user_auth_required', 'anon', 401),
            ('change_user_forbidden', 'change', 403),
            ('delete_user_forbidden', 'delete', 403),
            ('different_organization_user_forbidden', 'different_tenancy', 403),
            ('no_permission_user_forbidden', 'no_permissions', 403),
            ('view_user_forbidden', 'view', 403),
        ]


    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_add,
        ids=[test_name for test_name, user, expected in permission_no_add]
    )
    def test_permission_no_add(
        self,
        test_name, user, expected
    ):
        pytest.xfail( reason = 'Ticket dependencies must be added via slash command.' )
