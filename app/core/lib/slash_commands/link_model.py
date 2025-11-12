import importlib
import re

from django.apps import apps
from django.core.exceptions import ValidationError



class CommandLinkModelTicket:
    # This summary is used for the user documentation
    """Link an item to the current ticket. Supports all ticket 
relations: blocked by, blocks and related.
The command keyword is `link` along with the model reference, i.e. `$<type>-<number>`.

Valid commands are as follows:

- /link $device-1

- /link $cluster-55

You can also stack model references. i.e. `/link $device-1 $cluster-55 $software-2254`

Available model types for linking are that same as exists for model references. Please see the [markdown](./markdown.md) documentation:

For this command to process the following conditions must be met:

- There is a `<new line>` (`\n`) char immediatly before the slash `/`

- There is a `<space>` char after the command keyword, i.e. `/link<space>$device-101`
"""


    link_model: str = r'\/(?P<full>(?P<command>[link]+)(?P<models>(\s\$(?P<type>[a-z_]+)-(?P<id>\d+)))+)[\s]?'

    single_model: str = r'\$(?P<type>[a-z_]+)-(?P<id>\d+)'


    def command_link_model(self, match) -> str:
        """/link processor

        Slash command processor for linking a model to a ticket.

        Args:
            match (re.Match): Named group matches

        Returns:
            str: The matched string if no match could be made
            None: On successfully processing the command
        """

        ticket = self

        base_model = getattr(self, '_base_model', None)

        if base_model:
            base_model = base_model._meta.model_name

        if base_model == 'ticketcommentbase':

            ticket = self.ticket


        found_items = re.findall(self.single_model, match.group('full'))

        try:

            for model_type, model_id in found_items:

                try:

                    model = self.get_model( model_type )

                    model = apps.get_model(
                        app_label = model._meta.app_label,
                        model_name = f'{model._meta.object_name}Ticket'.lower()
                    )

                    if not model:

                        return str(match.string[match.start():match.end()])


                    model.objects.create(
                        ticket = ticket,
                        model_id = int(model_id)
                    )


                except ValidationError as err:

                    error = err.get_codes().get('non_field_errors', None)

                    if error is not None:

                        if error[0] != 'unique':

                            raise ValidationError(
                                message = err.message,
                                code = err.code
                            )


            return None

        except Exception as e:

            return str(match.string[match.start():match.end()])



    def get_model(self, model_type: str) -> object:
        """Get the model assiated with the model_tag

        Args:
            model_type (str): model tag to search for

        Returns:
            object: model that belongs to the model_tag
        """

        for obj_model in apps.get_models():

            if model_type == getattr(obj_model, 'model_tag', '-not_model-'):
                return obj_model


        return None
