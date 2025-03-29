import re

from core import exceptions as centurion_exceptions



class CommandRelatedTicket:
    # This summary is used for the user documentation
    """Add to the current ticket a relationship to another ticket. Supports all ticket 
relations: blocked by, blocks and related.
The command keywords are `relate`, `blocks` and `blocked_by` along with the ticket
reference, i.e. `#<ticket-number>`.

Valid commands are as follows:

- /relate #1

- /blocks #1

- /blocked_by #1

You can also stack ticket references. i.e. `/relate #1 #10 #500`

For this command to process the following conditions must be met:

- The slash `/` is the first character on the line

- There is a `<space>` char after the command keyword, i.e. `/relate<space>#1`
"""


    related_ticket: str = r'\/(?P<full>(?P<command>[relate|blocks|blocked_by]+)(\s\#(?P<ticket>\d+))+)\s?'

    related_ticket_single_item: str = r'\#(?P<ticket>\d+)'


    def command_related_ticket(self, match) -> str:
        """/relate, /blocks and /blocked_by processor

        Slash command usage within a ticket description will add an action comment with the
        time spent. For a ticket comment, it's duration field is set to the duration valuee calculated.

        Args:
            match (re.Match): Named group matches

        Returns:
            str: The matched string if the duration calculation is `0`
            None: On successfully processing the command
        """

        command = match.group('command')

        found_items = re.findall(self.related_ticket_single_item, match.group('full'))

        try:

            for ticket_id in found_items:

                try:

                    if ticket_id is not None:

                        from core.serializers.ticket_related import RelatedTickets, RelatedTicketModelSerializer

                        if command == 'relate':

                            how_related = RelatedTickets.Related.RELATED.value

                        elif command == 'blocks':

                            how_related = RelatedTickets.Related.BLOCKS.value

                        elif command == 'blocked_by':

                            how_related = RelatedTickets.Related.BLOCKED_BY.value

                        else:

                            #ToDo: Add logging that the slash command could not be processed.

                            return str(match.string[match.start():match.end()])


                        if str(self._meta.verbose_name).lower() == 'ticket':

                            from_ticket = self

                            to_ticket = self.__class__.objects.get(pk = ticket_id)

                        elif str(self._meta.verbose_name).lower() == 'ticket comment':

                            from_ticket = self.ticket

                            to_ticket = self.ticket.__class__.objects.get(pk = ticket_id)


                        item = RelatedTicketModelSerializer(
                            data = {
                                'from_ticket_id': from_ticket.id,
                                'how_related': int(how_related),
                                'to_ticket_id': to_ticket.id,
                                'organization': from_ticket.organization.id
                            }
                        )

                        if item.is_valid( raise_exception = False ):

                            item.save()


                except centurion_exceptions.ValidationError as err:

                    error = err.get_codes().get('non_field_errors', None)

                    if error is not None:

                        if error[0] != 'unique':

                            raise centurion_exceptions.ValidationError(
                                detail = err.detail,
                                code = err.get_codes()
                            )

        except Exception as e:

            #ToDo: Add logging that the slash command could not be processed.

            return str(match.string[match.start():match.end()])

        return None
