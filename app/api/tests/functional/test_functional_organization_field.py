import pytest

from api.serializers.common import OrganizationField



class MockRequest:
    """Stand-in for the DRF request object.

    Carries the `app_settings` object (attached by the tenancy middleware),
    whose `global_organization` is a real `Tenant` so the inter-object calls
    are exercised for real.
    """

    app_settings = None


    class MockAppSettings:

        global_organization = None


        def __init__(self, global_organization):

            self.global_organization = global_organization


    def __init__(self, global_organization):

        self.app_settings = self.MockAppSettings( global_organization )



@pytest.mark.api
@pytest.mark.fields
@pytest.mark.functional
class OrganizationFieldTestCases:
    """Functional tests for the `OrganizationField` serializer field.

    These exercise the real inter-object behaviour: the `Tenant` manager, the
    queryset `exclude` and `request.app_settings.global_organization`.
    """


    @pytest.fixture
    def organization_field(self, model_tenant, kwargs_tenant):
        """An `OrganizationField` whose context reports a freshly created
        `Tenant` as the configured global organization.
        """

        global_organization = model_tenant.objects.create( **kwargs_tenant() )

        field = OrganizationField()

        field._context = { 'request': MockRequest( global_organization ) }

        yield field

        del field._context


    def test_get_queryset_includes_non_global_organization(self,
        organization_field, model_tenant, kwargs_tenant
    ):
        """OrganizationField Check

        Ensure organizations that are not the configured global organization
        are still returned by `get_queryset`.
        """

        other_organization = model_tenant.objects.create( **kwargs_tenant() )

        assert other_organization in organization_field.get_queryset()



class OrganizationFieldInheritedCases(
    OrganizationFieldTestCases
):

    pass



@pytest.mark.module_api
class OrganizationFieldPyTest(
    OrganizationFieldTestCases
):

    pass
