import pytest

from api.serializers.common import CommonModelSerializer, OrganizationField



class MockRequest:
    """Stand-in for the DRF request object.

    Mirrors the object the field consumes: a request carrying the
    `app_settings` object (attached by the tenancy middleware) which in turn
    holds the configured `global_organization`.
    """

    app_settings = None


    class MockAppSettings:

        global_organization = None


        class MockOrganization:

            id = 4321


        def __init__(self):

            self.global_organization = self.MockOrganization()


    def __init__(self):

        self.app_settings = self.MockAppSettings()



@pytest.mark.api
@pytest.mark.fields
@pytest.mark.unit
class OrganizationFieldTestCases:
    """Unit tests for the `OrganizationField` serializer field."""


    @pytest.fixture
    def organization_field(self):
        """An `OrganizationField` whose context reports a global organization
        with id `MockRequest.MockAppSettings.MockOrganization.id`.
        """

        field = OrganizationField()

        field._context = { 'request': MockRequest() }

        yield field

        del field._context


    def test_get_queryset_sources_from_the_tenant_manager(self, mocker,
        organization_field
    ):
        """OrganizationField Check

        Ensure `get_queryset` sources the organizations from the `Tenant`
        manager. If the source manager is changed, this must fail.
        """

        tenant_objects = mocker.patch('api.serializers.common.Tenant.objects')

        organization_field.get_queryset()

        tenant_objects.all.assert_called()


    def test_get_queryset_excludes_global_organization(self, mocker,
        organization_field
    ):
        """OrganizationField Check

        Ensure `get_queryset` excludes the configured global organization from
        the queryset by its id. See #406 / #419.
        """

        tenant_objects = mocker.patch('api.serializers.common.Tenant.objects')

        organization_field.get_queryset()

        assert tenant_objects.all.return_value.exclude.call_args.kwargs['id'] == MockRequest.MockAppSettings.MockOrganization.id


    def test_common_model_serializer_uses_organization_field(self):
        """OrganizationField Check

        Ensure the organization field used by `CommonModelSerializer` (which
        every tenancy serializer, and therefore every endpoint, inherits) is an
        `OrganizationField`, so the filtering tested above is the one in use.
        """

        assert isinstance(
            CommonModelSerializer._declared_fields['organization'],
            OrganizationField
        )



class OrganizationFieldInheritedCases(
    OrganizationFieldTestCases
):

    pass



@pytest.mark.module_api
class OrganizationFieldPyTest(
    OrganizationFieldTestCases
):

    pass
