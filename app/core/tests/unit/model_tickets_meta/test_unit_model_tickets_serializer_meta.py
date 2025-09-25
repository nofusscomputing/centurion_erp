import pytest

from core.tests.unit.model_tickets.test_unit_model_tickets_serializer import (
    ModelTicketSerializerInheritedCases
)



@pytest.mark.model_modelticketmeta
class ModelTicketMetaSerializerTestCases(
    ModelTicketSerializerInheritedCases
):
    pass


class ModelTicketMetaSerializerInheritedCases(
    ModelTicketMetaSerializerTestCases
):
    pass


@pytest.mark.module_core
class ModelTicketMetaSerializerPyTest(
    ModelTicketMetaSerializerTestCases
):
    pass
