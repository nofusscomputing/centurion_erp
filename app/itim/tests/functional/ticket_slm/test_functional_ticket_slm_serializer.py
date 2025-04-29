from django.test import TestCase

from core.tests.functional.ticket_base.test_functional_ticket_base_serializer import TicketBaseSerializerInheritedCases

from itim.serializers.ticket_slm import (
    SLMTicket,
    ModelSerializer
)



class SerializerTestCases(
    TicketBaseSerializerInheritedCases,
):

    model = SLMTicket

    create_model_serializer = ModelSerializer

    valid_data: dict = {
        'ttr': 2,
        'tto': 3,
    }



class SLMTicketSerializerInheritedCases(
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



class SLMTicketSerializerTest(
    SerializerTestCases,
    TestCase,
):

    pass
