from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.serializers.itim.problem import ProblemTicketSerializer
from api.views.core.tickets import View



class View(View):

    _ticket_type:str = 'problem'


    @extend_schema(
        summary='Create a ticket',
        description = """This model includes all of the ticket types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        request = ProblemTicketSerializer,
        responses = {
            201: OpenApiResponse(
                response = ProblemTicketSerializer,
            ),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)



    @extend_schema(
        summary='Fetch all tickets',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProblemTicketSerializer
            )
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected ticket',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProblemTicketSerializer
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)





    def get_view_name(self):

        if self.detail:
            return "Problem Ticket"
        
        return 'Problem Tickets'
