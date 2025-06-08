import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)


class TenantSerializerTestCases(
    SerializerTestCases
):
    pass



@pytest.mark.model_tenant
@pytest.mark.module_access
class TenantSerializerPyTest(
    TenantSerializerTestCases
):
    pass