from django.test import TestCase

from itim.serializers.ticket_request import (
    RequestTicket,
    ModelSerializer
)
from itim.tests.functional.ticket_slm.test_functional_ticket_slm_serializer import SLMTicketSerializerInheritedCases



class SerializerTestCases(
    SLMTicketSerializerInheritedCases,
):

    model = RequestTicket

    create_model_serializer = ModelSerializer



class TicketBaseSerializerInheritedCases(
    SerializerTestCases,
):

    model = None
    """Model to test"""

    valid_data: dict = {}
    """Valid data used by serializer to create object"""


    @classmethod
    def setUpTestData(self):

        self.valid_data = {
            **super().valid_data,
            **self.valid_data
        }

        super().setUpTestData()



class TicketBaseSerializerTest(
    SerializerTestCases,
    TestCase,
):

    pass
