import re

from .duration import Duration
from .related_ticket import CommandRelatedTicket    # depreciated model
from .linked_model import CommandLinkedModel    # depreciated model
# from .link_model import CommandLinkModelTicket
from .ticket_dependency import CommandTicketDependency


class SlashCommands(
    Duration,
    CommandRelatedTicket,    # depreciated model
    CommandLinkedModel,    # depreciated model
    # CommandLinkModelTicket,
    CommandTicketDependency,
):
    """Slash Commands Base Class
    
    This class in intended to be included in the following models:
    
    - Ticket
    
    - TicketComment

    Testing of regex can be done at https://pythex.org/
    """

    command: str = r'^\/(?P<full>(?P<command>[a-z\_]+).+)'


    def slash_command(self, markdown:str) -> str:
        """ Slash Commands Processor

        Markdown text that contains a slash command is passed to this function and on the processing
        of any valid slash command, the slash command will be removed from the markdown.

        If any error occurs when attempting to process the slash command, it will not be removed from
        the markdown. This is by design so that the "errored" slash command can be inspected.

        Args:
            markdown (str): un-processed Markdown

        Returns:
            str: Markdown without the slash command text.
        """

        nl = '\n'

        if '\r\n' in markdown:

            nl = '\r\n'

            lines = str(markdown).split(nl)

        else:

            lines = str(markdown).split(nl)


        processed_lines = ''

        base_model = getattr(self, '_base_model', None)

        if base_model:
            base_model = base_model._meta.model_name


        for line in lines:

            line = str(line).strip()

            search = re.match(self.command, line)

            if search is not None:

                command = search.group('command')

                returned_line = ''

                if(
                    command == 'spend'
                    or command == 'spent'
                ):

                    returned_line = re.sub(self.time_spent, self.command_duration, line)

                elif command == 'link':

                    if base_model in ['ticketbase', 'ticketcommentbase']:

                        # returned_line = re.sub(self.link_model, self.command_link_model, line)
                        pass

                    else:    # Depreciated Ticket Model and Command

                        returned_line = re.sub(self.linked_item, self.command_linked_model, line)


                elif(
                    command == 'relate'
                    or command == 'blocks'
                    or command == 'blocked_by'
                ):

                    if base_model in ['ticketbase', 'ticketcommentbase']:

                        returned_line = re.sub(self.ticket_dependency, self.command_ticket_dependency, line)

                    else:    # Depreciated Ticket Model and Command

                        returned_line = re.sub(self.related_ticket, self.command_related_ticket, line)


                if returned_line != '':

                    processed_lines += line + nl


            else:

                processed_lines += line + nl


        return str(processed_lines).strip()
