from typing import Any


import re

from django.apps import apps
from django.db.models import ObjectDoesNotExist

from core.fields import CharField
from core.lib.slash_commands.link_model import CommandLinkModelTicket



class MarkdownField(CharField):


    style_class: str = None
    """ UI field Additional CSS classes

    Format for this value is Sapce Seperated Value (SSV)
    """

    def __init__(
        self,
        multiline = True,
        style_class = None,
        **kwargs
    ):

        self.style_class = style_class

        super().__init__(multiline = multiline, **kwargs)



    def get_model(self, model_tag:str):
        """Get the model that has the specified model_tag

        A permission check is done to ensure that the user has the required
        permission to view the model.

        Args:
            model_tag (str): Model tag to use to find the model

        Returns:
            CenturionModel: The model that has the model_tag
            None: User is missing the required permissions
        """

        for model in apps.get_models():

            if getattr(model, 'model_tag', '') == model_tag:

                if self.context['request'].user.has_perm(
                    permission = f'{model._meta.app_label}.view_{model._meta.model_name}',
                    tenancy_permission = False
                ):

                    return model

                else:
                    return None

        return None


    def get_markdown_render(self, markdown: str) -> dict:
        """Markdown Render

        Creates the dict that the UI uses to render any custom markdown tags.
        If any markdown object is invalid, then it should be ignored. In the
        same token, if the user does not have the permission in the models
        entity, the object should also not be returned.

        Args:
            markdown (str): Markdown string to check

        Returns:
            dict: All required fields for the UI to render the markdown.
        """

        from core.models.ticket_base import TicketBase
        from core.models.model_tickets import ModelTicket

        markdown_render: dict = {
            'markdown': markdown,
            'render': {}
        }

        linked_tickets = re.findall(r'(?P<ticket>#(?P<number>\d+))', markdown)

        model_links = re.findall(r'(\$(?P<type>[a-z_]+)-(?P<id>\d+))', markdown)

        models: dict = {}

        for tag, model_type, model_id in model_links:

            try:

                model = self.get_model(model_tag = model_type)

                if model is None:
                    continue

                obj = model.objects.get(
                    id = int(model_id)
                )


                if self.context['request'].user.has_perm(
                    permission = f'{obj._meta.app_label}.view_{obj._meta.model_name}',
                    tenancy = obj.get_organization()
                ):

                    if model_type not in models:

                        models.update({ model_type: {} })


                    models[model_type].update({
                        str(model_id): {
                            'title': str(obj),
                            'url': str(obj.get_url( relative = True )).replace('/api/v2', '')
                        }
                    })

            except ObjectDoesNotExist:    # skip for invalid object
                pass


        if models:

            markdown_render['render'].update({
                    'models': models,
                })


        tickets: dict = {}

        for ticket_markdown, number in linked_tickets:

            try:

                item = TicketBase.objects.get( pk = number ).get_related_model()


                if self.context['request'].user.has_perm(
                    permission = f'{item._meta.app_label}.view_{item._meta.model_name}',
                    tenancy = item.organization
                ):


                    tickets.update({
                        number: {
                            'status': TicketBase.TicketStatus(item.status).label,
                            'ticket_type': item.ticket_type,
                            'title': str(item),
                            'url': str(item.get_url( relative = True )).replace('/api/v2', '')
                        }
                    })

            except ObjectDoesNotExist:    # Dont provide render for invalid ticket
                pass


        if tickets:

            markdown_render['render'].update({
                    'tickets': tickets,
                })


        return markdown_render



    def to_representation(self, value):

        return self.get_markdown_render(markdown = super().to_representation(value))
