import re

from core import exceptions as centurion_exceptions



class CommandLinkedModel:
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


    linked_item: str = r'\/(?P<full>(?P<command>[link]+)(?P<models>(\s\$(?P<type>[a-z_]+)-(?P<id>\d+)))+)[\s]?'

    single_item: str = r'\$(?P<type>[a-z_]+)-(?P<id>\d+)'


    def command_linked_model(self, match) -> str:
        """/link processor

        Slash command usage within a ticket description will add an action comment with the
        time spent. For a ticket comment, it's duration field is set to the duration valuee calculated.

        ## Adding New Item

        Adding a new item to be linked also requires that you update:
        
        - `__str__` function within `core.models.ticket.ticket_linked_item.TicketLinkedItem`

        - `get_item` function within `app.core.serializar.ticket_linked_item.TicketLinkedItemViewSerializer`

        Args:
            match (re.Match): Named group matches

        Returns:
            str: The matched string if the duration calculation is `0`
            None: On successfully processing the command
        """

        ticket = self

        if str(self._meta.verbose_name).lower() == 'ticket comment':

            ticket = self.ticket

        found_items = re.findall(self.single_item, match.group('full'))

        try:

            for model_type, model_id in found_items:

                try:

                    model, item_type = self.get_model( model_type )

                    if not model:

                        return str(match.string[match.start():match.end()])


                    if model:

                        item = model.objects.get(
                            pk = model_id
                        )

                        from core.serializers.ticket_linked_item import TicketLinkedItemModelSerializer

                        serializer = TicketLinkedItemModelSerializer(
                            data = {
                                'organization': ticket.organization,
                                'ticket': ticket.id,
                                'item_type': item_type,
                                'item': item.id
                            }
                        )

                        if serializer.is_valid( raise_exception = True ):

                            serializer.save()

                except centurion_exceptions.ValidationError as err:

                    error = err.get_codes().get('non_field_errors', None)

                    if error is not None:

                        if error[0] != 'unique':

                            raise centurion_exceptions.ValidationError(
                                detail = err.detail,
                                code = err.get_codes()
                            )



            return None

        except Exception as e:

            return str(match.string[match.start():match.end()])

        return None


    def get_model(self, model_type) -> tuple():

        model = None

        item_type = None

        from core.models.ticket.ticket_linked_items import TicketLinkedItem

        if model_type == 'asset':

            from accounting.models.asset_base import AssetBase

            model = AssetBase

            item_type = TicketLinkedItem.Modules.ASSET

        elif model_type == 'cluster':

            from itim.models.clusters import Cluster

            model = Cluster

            item_type = TicketLinkedItem.Modules.CLUSTER

        elif model_type == 'config_group':

            from config_management.models.groups import ConfigGroups

            model = ConfigGroups

            item_type = TicketLinkedItem.Modules.CONFIG_GROUP

        elif model_type == 'device':

            from itam.models.device import Device

            model = Device

            item_type = TicketLinkedItem.Modules.DEVICE

        elif model_type == 'entity':

            from access.models.entity import Entity

            model = Entity

            item_type = TicketLinkedItem.Modules.ENTITY

        elif model_type == 'feature_flag':

            from devops.models.feature_flag import FeatureFlag

            model = FeatureFlag

            item_type = TicketLinkedItem.Modules.FEATURE_FLAG

        elif model_type == 'git_repository':

            from devops.models.git_repository.base import GitRepository

            model = GitRepository

            item_type = TicketLinkedItem.Modules.GIT_REPOSITORY

        elif model_type == 'it_asset':

            from itam.models.itam_asset_base import ITAMAssetBase

            model = ITAMAssetBase

            item_type = TicketLinkedItem.Modules.IT_ASSET

        elif model_type == 'kb':

            from assistance.models.knowledge_base import KnowledgeBase

            model = KnowledgeBase

            item_type = TicketLinkedItem.Modules.KB

        elif  model_type == 'operating_system':

            from itam.models.operating_system import OperatingSystem

            model = OperatingSystem

            item_type = TicketLinkedItem.Modules.OPERATING_SYSTEM

        elif model_type == 'tenant':

            from access.models.tenant import Tenant

            model = Tenant

            item_type = TicketLinkedItem.Modules.ORGANIZATION

        elif  model_type == 'role':

            from access.models.role import Role

            model = Role

            item_type = TicketLinkedItem.Modules.ROLE

        elif model_type == 'service':

            from itim.models.services import Service

            model = Service

            item_type = TicketLinkedItem.Modules.SERVICE

        elif model_type == 'software':

            from itam.models.software import Software

            model = Software

            item_type = TicketLinkedItem.Modules.SOFTWARE

        elif model_type == 'software_version':

            from itam.models.software import SoftwareVersion

            model = SoftwareVersion

            item_type = TicketLinkedItem.Modules.SOFTWARE_VERSION

        elif model_type == 'team':

            from access.models.team import Team

            model = Team

            item_type = TicketLinkedItem.Modules.TEAM

        elif model_type == 'project_state':

            from project_management.models.project_states import ProjectState

            model = ProjectState

            item_type = TicketLinkedItem.Modules.PROJECT_STATE

        elif model_type == 'ticket_category':

            from core.models.ticket.ticket_category import TicketCategory

            model = TicketCategory

            item_type = TicketLinkedItem.Modules.TICKET_CATEGORY

        elif model_type == 'ticket_comment_category':

            from core.models.ticket.ticket_comment_category import TicketCommentCategory

            model = TicketCommentCategory

            item_type = TicketLinkedItem.Modules.TICKET_COMMENT_CATEGORY


        return tuple([
            model,
            item_type
        ])
