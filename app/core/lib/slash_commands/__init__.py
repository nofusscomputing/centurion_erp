import re

from .duration import Duration
from .related_ticket import CommandRelatedTicket
from .linked_model import CommandLinkedModel


class SlashCommands(
    Duration,
    CommandRelatedTicket,
    CommandLinkedModel,
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

        if '\n' in markdown:

            lines = str(markdown).split('\n')

        else:

            lines = str('\n' + markdown + '\n').split('\n')

        processed_lines = ''

        for line in lines:

            search = re.match(self.command, line)

            if search is not None:

                command = search.group('command')

                returned_line = ''

                if command == 'spend':

                    returned_line = re.sub(self.time_spent, self.command_duration, line)

                elif command == 'link':

                    returned_line = re.sub(self.linked_item, self.command_linked_model, line)

                elif(
                    command == 'relate'
                    or command == 'blocks'
                    or command == 'blocked_by'
                ):

                    returned_line = re.sub(self.related_ticket, self.command_related_ticket, line)

                if returned_line != '':

                    processed_lines += line + '\n'

            else:

                processed_lines += line + '\n'

        return str(processed_lines).strip()
