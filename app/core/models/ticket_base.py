import datetime
import difflib

from django.apps import apps
from django.conf import settings
from django.db import models

from access.fields import AutoLastModifiedField
from access.models.entity import Entity

from core import exceptions as centurion_exceptions
from core.classes.badge import Badge
from core.lib.slash_commands import SlashCommands
from core.middleware.get_request import get_request
from core.models.centurion import CenturionModel
from core.models.ticket.ticket_category import TicketCategory
from core.models.ticket.ticket_enum_values import TicketValues

from project_management.models.project_milestone import Project, ProjectMilestone



class TicketBase(
    SlashCommands,
    CenturionModel,
):

    _after: dict
    """History After
    Data after save was called
    """

    _audit_enabled = False

    @property
    def _base_model(self):

        return TicketBase

    _before: dict
    """History Before
    Data before save was called
    """

    _notes_enabled = False

    _ticket_linkable = False

    model_notes = None

    model_tag = 'ticket'

    save_model_history: bool = False

    url_model_name = 'ticketbase'

    class Ticket_ExternalSystem(models.IntegerChoices): # <null|github|gitlab>
        GITHUB   = TicketValues.ExternalSystem._GITHUB_INT, TicketValues.ExternalSystem._GITHUB_VALUE
        GITLAB   = TicketValues.ExternalSystem._GITLAB_INT, TicketValues.ExternalSystem._GITLAB_VALUE

        CUSTOM_1 = TicketValues.ExternalSystem._CUSTOM_1_INT, TicketValues.ExternalSystem._CUSTOM_1_VALUE
        CUSTOM_2 = TicketValues.ExternalSystem._CUSTOM_2_INT, TicketValues.ExternalSystem._CUSTOM_2_VALUE
        CUSTOM_3 = TicketValues.ExternalSystem._CUSTOM_3_INT, TicketValues.ExternalSystem._CUSTOM_3_VALUE
        CUSTOM_4 = TicketValues.ExternalSystem._CUSTOM_4_INT, TicketValues.ExternalSystem._CUSTOM_4_VALUE
        CUSTOM_5 = TicketValues.ExternalSystem._CUSTOM_5_INT, TicketValues.ExternalSystem._CUSTOM_5_VALUE
        CUSTOM_6 = TicketValues.ExternalSystem._CUSTOM_6_INT, TicketValues.ExternalSystem._CUSTOM_6_VALUE
        CUSTOM_7 = TicketValues.ExternalSystem._CUSTOM_7_INT, TicketValues.ExternalSystem._CUSTOM_7_VALUE
        CUSTOM_8 = TicketValues.ExternalSystem._CUSTOM_8_INT, TicketValues.ExternalSystem._CUSTOM_8_VALUE
        CUSTOM_9 = TicketValues.ExternalSystem._CUSTOM_9_INT, TicketValues.ExternalSystem._CUSTOM_9_VALUE



    class TicketStatus(models.IntegerChoices): # <draft|open|closed|in progress|assigned|solved|invalid>
        """ Ticket Status

        To add more status', override this class within your sub-model
        """

        DRAFT             = TicketValues._DRAFT_INT, TicketValues._DRAFT_STR
        NEW               = TicketValues._NEW_INT, TicketValues._NEW_STR
        ASSIGNED          = TicketValues._ASSIGNED_INT, TicketValues._ASSIGNED_STR
        ASSIGNED_PLANNING = TicketValues._ASSIGNED_PLANNING_INT, TicketValues._ASSIGNED_PLANNING_STR
        PENDING           = TicketValues._PENDING_INT, TicketValues._PENDING_STR
        SOLVED            = TicketValues._SOLVED_INT, TicketValues._SOLVED_STR
        CLOSED            = TicketValues._CLOSED_INT, TicketValues._CLOSED_STR
        # DUPLICATE         = 
        INVALID           = TicketValues._INVALID_INT, TicketValues._INVALID_STR



    class TicketUrgency(models.IntegerChoices): # <null|github|gitlab>
        VERY_LOW  = '1', 'Very Low'
        LOW       = '2', 'Low'
        MEDIUM    = '3', 'Medium'
        HIGH      = '4', 'High'
        VERY_HIGH = '5', 'Very High'



    class TicketImpact(models.IntegerChoices):
        VERY_LOW  = '1', 'Very Low'
        LOW       = '2', 'Low'
        MEDIUM    = '3', 'Medium'
        HIGH      = '4', 'High'
        VERY_HIGH = '5', 'Very High'



    class TicketPriority(models.IntegerChoices):
        VERY_LOW  = TicketValues.Priority._VERY_LOW_INT, TicketValues.Priority._VERY_LOW_VALUE
        LOW       = TicketValues.Priority._LOW_INT, TicketValues.Priority._LOW_VALUE
        MEDIUM    = TicketValues.Priority._MEDIUM_INT, TicketValues.Priority._MEDIUM_VALUE
        HIGH      = TicketValues.Priority._HIGH_INT, TicketValues.Priority._HIGH_VALUE
        VERY_HIGH = TicketValues.Priority._VERY_HIGH_INT, TicketValues.Priority._VERY_HIGH_VALUE
        MAJOR     = TicketValues.Priority._MAJOR_INT, TicketValues.Priority._MAJOR_VALUE



    class TicketSource(models.IntegerChoices):
        """Source of the comment"""

        DIRECT          = '1', 'Direct'
        EMAIL           = '2', 'E-Mail'
        HELPDESK        = '3', 'Helpdesk'
        PHONE           = '4', 'Phone'
        SERVICE_CATALOG = '5', 'Service Catalog'
        SMS             = '6', 'SMS Message'



    class Meta:

        ordering = [
            'id'
        ]

        permissions = [
            ('import_ticketbase', 'Can import a ticket base'),
            ('purge_ticketbase', 'Can purge a ticket base'),
            ('triage_ticketbase', 'Can triage a ticket base'),
        ]

        sub_model_type = 'ticket'

        unique_together = ('external_system', 'external_ref',)

        verbose_name = "Ticket"

        verbose_name_plural = "Tickets"


    def validate_not_null(field):

        if field is None:

            return False

        return True


    external_system = models.IntegerField(
        blank = True,
        choices = Ticket_ExternalSystem,
        help_text = 'External system this item derives',
        null = True,
        verbose_name = 'External System',
    ) 

    external_ref = models.IntegerField(
        blank = True,
        help_text = 'External System reference',
        null = True,
        verbose_name = 'Reference Number',
    ) # external reference or null. i.e. github issue number

    parent_ticket = models.ForeignKey(
        'self',
        blank = True,
        help_text = 'Parent of this ticket',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Parent Ticket'
    )

    @property
    def get_ticket_type(self):
        """Fetch the Ticket Type

        You can safely override this function as long as it's called or the
        logic is included in your over-ridden function.

        Returns:
            str: The models `Meta.verbose_name` in lowercase and without spaces
            None: The ticket is for the Base class. Used to prevent creating a base ticket.
        """

        ticket_type = str(self._meta.sub_model_type).lower().replace(' ', '_')

        if ticket_type == 'ticket':

            return None

        return ticket_type


    def get_ticket_type_choices():

        choices = []

        if apps.ready:

            all_models = apps.get_models()

            for model in all_models:

                if isinstance(model, TicketBase) or issubclass(model, TicketBase):

                    choices += [ (model._meta.sub_model_type, model._meta.verbose_name) ]


        return choices


    ticket_type = models.CharField(
        blank = True,
        choices = get_ticket_type_choices,
        # default = get_ticket_type_default,
        default = Meta.sub_model_type,
        help_text = 'Ticket Type. (derived from ticket model)',
        max_length = 30,
        null = False,
        validators = [
            validate_not_null
        ],
        verbose_name = 'Ticket Type',
    )

    status = models.IntegerField( # will require validation by ticket type as status for types will be different
        blank = False,
        choices = TicketStatus,
        default = TicketStatus.NEW,
        help_text = 'Status of ticket',
        null = False,
        verbose_name = 'Status',
    )

    @property
    def status_badge(self):

        text:str = 'Add'

        if self.status:

            text:str = str(self.get_status_display())
            style:str = text.replace('(', '')
            style = style.replace(')', '')
            style = style.replace(' ', '_')

        return Badge(
            icon_name = f'ticket_status_{style.lower()}',
            icon_style = f'ticket-status-icon ticket-status-icon-{style.lower()}',
            text = text,
            text_style = f'ticket-status-text badge-text-ticket_status-{style.lower()}',
        )

    category = models.ForeignKey(
        TicketCategory,
        blank = True,
        help_text = 'Category for this ticket',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Category',
    )

    title = models.CharField(
        blank = False,
        help_text = "Title of the Ticket",
        max_length = 150,
        unique = True,
        verbose_name = 'Title',
    )

    description = models.TextField(
        blank = True,
        help_text = 'Description for the ticket.',
        null = True,
        verbose_name = 'Description',
    ) # text, markdown


    private = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this ticket private',
        null = False,
        verbose_name = 'Private',
    )

    @property
    def ticket_duration(self) -> int:

        comments = self.get_comments()

        duration = comments.aggregate(models.Sum('duration'))['duration__sum']

        if duration is None:

            duration = 0

        return int(duration)


    @property
    def ticket_estimation(self) -> int:

        comments = self.get_comments()

        estimation = comments.aggregate(models.Sum('estimation'))['estimation__sum']

        if estimation is None:

            estimation = 0

        return int(estimation)


    project = models.ForeignKey(
        Project,
        blank= True,
        help_text = 'Assign to a project',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Project',
    )



    def get_milestone_choices():
        # does not seem to work for model field (metadata.field.choices)

        choices = []

        for project in Project.objects.prefetch_related('projectmilestone_set'):

            milestone_choices = []

            for milestone in project.projectmilestone_set.all():

                milestone_choices += [ (milestone.id, milestone.name) ]

            if len(milestone_choices) > 0:

                choices += [ (project.name, ( milestone_choices ) ) ]


        return choices


    milestone = models.ForeignKey(
        ProjectMilestone,
        blank = True,
        # choices = get_milestone_choices,
        help_text = 'Assign to a milestone',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Project Milestone',
    )

    urgency = models.IntegerField(
        blank = True,
        choices=TicketUrgency,
        default=TicketUrgency.VERY_LOW,
        help_text = 'How urgent is this tickets resolution for the user?',
        null=True,
        verbose_name = 'Urgency',
    )


    @property
    def urgency_badge(self):

        if self.urgency is None:

            return None

        text = self.get_urgency_display()

        return Badge(
            icon_name = 'circle',
            icon_style = f"status {text.lower().replace(' ', '-')}",
            text = text,
            text_style = '',
        )


    impact = models.IntegerField(
        blank = True,
        choices=TicketImpact,
        default=TicketImpact.VERY_LOW,
        help_text = 'End user assessed impact',
        null=True,
        verbose_name = 'Impact',
    ) 


    @property
    def impact_badge(self):

        if self.impact is None:

            return None


        text = self.get_impact_display()

        return Badge(
            icon_name = 'circle',
            icon_style = f"status {text.lower().replace(' ', '-')}",
            text = text,
            text_style = '',
        )


    priority = models.IntegerField(
        blank = True,
        choices=TicketPriority,
        default=TicketPriority.VERY_LOW,
        help_text = 'What priority should this ticket for its completion',
        null=True,
        verbose_name = 'Priority',
    ) 


    @property
    def priority_badge(self):

        if self.priority is None:

            return None

        text = self.get_priority_display()

        return Badge(
            icon_name = 'circle',
            icon_style = f"status {text.lower().replace(' ', '-')}",
            text = text,
            text_style = '',
        )


    opened_by = models.ForeignKey(
        Entity,
        blank = True,
        help_text = 'Who is the ticket for',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'ticket_opened',
        verbose_name = 'Opened By',
    )

    subscribed_to = models.ManyToManyField(
        Entity,
        blank = True,
        help_text = 'Users / Groups subscribed to the ticket',
        # on_delete = models.PROTECT,
        related_name = 'ticket_subscription',
        symmetrical = False,
        verbose_name = 'Users / Groups Subscribed',
    )

    assigned_to = models.ManyToManyField(
        Entity,
        blank= True,
        help_text = 'Users / Groups assigned to the ticket',
        # on_delete = models.PROTECT,
        related_name = 'ticket_assigned',
        symmetrical = False,
        verbose_name = 'Users / Groups Assigned',
    )

    planned_start_date = models.DateTimeField(
        blank = True,
        help_text = 'Planned start date.',
        null = True,
        verbose_name = 'Planned Start Date',
    )

    planned_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'Planned finish date',
        null = True,
        verbose_name = 'Planned Finish Date',
    )

    real_start_date = models.DateTimeField(
        blank = True,
        help_text = 'Real start date',
        null = True,
        verbose_name = 'Real Start Date',
    )

    real_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'Real finish date',
        null = True,
        verbose_name = 'Real Finish Date',
    )

    is_deleted = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Is the ticket deleted? And ready to be purged',
        null = False,
        verbose_name = 'Deleted',
    )

    is_solved = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Is this ticket solved?',
        null = False,
        verbose_name = 'Solved',
    )

    date_solved = models.DateTimeField(
        blank = True,
        help_text = 'Date ticket solved',
        null = True,
        verbose_name = 'Solved Date',
    )    # update everytime the ticket is solved.

    is_closed = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Is this ticket closed?',
        null = False,
        verbose_name = 'Closed',
    )

    date_closed = models.DateTimeField(
        blank = True,
        help_text = 'Date ticket closed',
        null = True,
        verbose_name = 'Closed Date',
    )

    modified = AutoLastModifiedField()



    # this model uses a custom page layout
    page_layout: list = []

    table_fields: list = [
        'id',
        'title',
        'status_badge',
        'priority_badge',
        'impact_badge',
        'urgency_badge',
        'opened_by',
        'organization',
        'created'
    ]


    def __str__(self):

        return self.title


    def clean(self):
        """Model Validation

        Raises:
            centurion_exceptions.ValidationError: Milestone project does not
                match the project assigned to the ticket.
            centurion_exceptions.ValidationError: Tried to solve a ticket when
                there are unresolved ticket comments.
        """

        if self.opened_by is None:

            raise centurion_exceptions.ValidationError(
                detail = {
                    'opened_by': 'This field is required.'
                },
                code = 'required'
            )


        if self.milestone:

            if self.milestone.project != self.project:

                raise centurion_exceptions.ValidationError(
                    detail = {
                        'milestone': f'Milestone is from project {self.milestone.project} when it should be from project {self.project}.'
                    },
                    code = 'milestone_different_project'
                )


        if(
            (
                self.status == self.TicketStatus.SOLVED
                and self.get_can_resolve( raise_exceptions = False )
            )
            or self.status == self.TicketStatus.INVALID
        ):

            self.is_solved = True


        elif(    # Re-Open Ticket
            ( self.is_solved or self.is_closed )
            and self.status != self.TicketStatus.CLOSED
            and self.status != self.TicketStatus.INVALID
            and self.status != self.TicketStatus.SOLVED
        ):

            if self.is_closed:

                self.is_closed = False

            if self.is_solved:

                self.is_solved = False


        elif not self.is_closed and self.status == self.TicketStatus.CLOSED:    # Close Ticket

            self.is_solved = True
            self.is_closed = True


        if self.is_solved:

            self.get_can_resolve( raise_exceptions = True )


        if self.is_closed:

            self.get_can_close( raise_exceptions = True )


        related_model = self.get_related_model()

        if related_model is None:

            related_model = self

        if self.ticket_type != str(related_model._meta.sub_model_type).lower().replace(' ', '_'):

            self.ticket_type = str(related_model._meta.sub_model_type).lower().replace(' ', '_')


        if self.date_solved is None and self.is_solved:

            self.date_solved = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()

        elif self.date_solved is not None and not self.is_solved:

            self.date_solved = None


        if self.date_closed is None and self.is_closed:

            self.date_closed = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()


        if self.date_closed is not None and not self.is_closed:

            self.date_closed = None


        self._before = {}

        try:
            self._before = self.__class__.objects.get(pk=self.pk).__dict__.copy()
        except Exception:
            pass

        super().clean()



    def clean_fields(self, exclude = None):

        if(
            self.description != ''
            and self.description is not None
        ):

            description = self.slash_command(self.description)

            if description != self.description:

                self.description = description


        return super().clean_fields(exclude = exclude)



    def get_can_close(self, raise_exceptions = False ) -> bool:

        if(
            (
                not self.get_can_resolve( raise_exceptions = False)
                or not self.is_solved
            )
            and not raise_exceptions
        ):

            return False

        elif(
            (
                not self.get_can_resolve( raise_exceptions = False)
                or not self.is_solved
            )
            and raise_exceptions
        ):

            raise centurion_exceptions.ValidationError(
                detail = {
                    'status': 'You cant close this ticket.'
                },
                code = 'ticket_close_failed_validation'
            )


        return True

    def get_can_resolve(self, raise_exceptions = False ) -> bool:

        ticket_comments = self.get_comments( include_threads = True )

        for comment in ticket_comments:

            if self.status == self.TicketStatus.INVALID:

                return True


            if not comment.is_closed and not raise_exceptions:

                return False

            elif not comment.is_closed and raise_exceptions:

                raise centurion_exceptions.ValidationError(
                    detail = {
                        'status': 'You cant solve a ticket when there are un-resolved comments.'
                    },
                    code = 'resolution_with_un_resolved_comment_denied'
                )

        return True


    def get_comments(self, include_threads = False):

        if hasattr(self, '_ticket_comments'):

            return self._ticket_comments

        from core.models.ticket_comment_base import TicketCommentBase

        if include_threads:

            self._ticket_comments = TicketCommentBase.objects.filter(
                ticket = self.id,
            ).order_by('created')

        else:

            self._ticket_comments = TicketCommentBase.objects.filter(
                ticket = self.id,
                parent = None,
            ).order_by('created')


        return self._ticket_comments



    def get_url_kwargs(self, many = False) -> dict:
        """Get URL Kwargs

        Fecth the kwargs required for building a models URL using the reverse
        method.

        **Note:** It's advisable that if you override this function, that you
        call it's super, so as not to duplicate code. That way each override
        builds up[on the parent `get_url_kwargs` function.

        Returns:
            dict: Kwargs required for reverse function to build a models URL.
        """

        kwargs = super().get_url_kwargs( many = many )

        if 'model_name' in kwargs:

            del kwargs['model_name']

        if str(self._meta.sub_model_type) != 'ticket':

            kwargs.update({
                'app_label': self._meta.app_label,
                'ticket_type': str(self._meta.sub_model_type),
            })


        return kwargs



    def create_action_comment(self) -> None:

        from core.models.ticket_comment_action import TicketCommentAction

        # request = get_request()
        request = None

        excluded_fields: list = [
            'created',
            'date_closed',
            'date_solved',
            'is_closed',
            'is_solved',
            'modified'
        ]
        changed_fields: list = []

        fields = [ value.name for value in self._meta.fields ]

        for field, value in self._before.items():

            if (
                self._before[field] != self._after[field]
                and field not in excluded_fields
                and (
                    field in fields
                    or (
                        str( field )[0:len(field)-3] in fields
                        and str( field ).endswith('_id')
                    )
                )
            ):

                changed_fields = changed_fields + [ field ]


        for field in changed_fields:

            if not request:
                # exit if no request obj.
                # this clause is temp until action commenting is setup/refactored
                return

            comment_text: str = None

            if field == 'category_id':

                value = 'None'

                if self._before[field]:

                    value = f"$ticket_category-{self._before[field]}"

                to_value = getattr(self.category, 'id', 'None')

                if to_value != 'None':

                    to_value = f"$ticket_category-{getattr(self.category, 'id', 'None')}"


                comment_text = f"changed category from {value} to {to_value}"

            elif field == 'impact':

                comment_text = f"changed {field} to {self.get_impact_display()}"

            elif field == 'urgency':

                comment_text = f"changed {field} to {self.get_urgency_display()}"

            elif field == 'priority':

                comment_text = f"changed {field} to {self.get_priority_display()}"


            elif field == 'organization':

                comment_text = f"Ticket moved from $organization-{self._before[field]} to $organization-{self._after[field]}"

            elif field == 'parent_ticket_id':

                value = 'None'

                if self._before[field]:

                    value = f"#{self._before[field]}"

                to_value = getattr(self.parent_ticket, 'id', 'None')

                if to_value != 'None':

                    to_value = f"#{getattr(self.parent_ticket, 'id', 'None')}"

                comment_text = f"Parent ticket changed from {value} to {to_value}"

            elif field == 'status':

                comment_text = f"changed {field} to {self.get_status_display()}"

            elif field == 'title':

                comment_text = f"Title changed ~~{self._before[field]}~~ to **{self._after[field]}**"

            elif field == 'project_id':

                value = 'None'

                if self._before[field]:

                    value = f"$project-{self._before[field]}"

                to_value = getattr(self.project, 'id', 'None')

                if to_value != 'None':

                    to_value = f"$project-{getattr(self.project, 'id', 'None')}"


                comment_text = f"changed project from {value} to {to_value}"

            elif field == 'milestone_id':

                value = 'None'

                if self._before[field]:

                    value = f"$milestone-{self._before[field]}"

                to_value = getattr(self.milestone, 'id', 'None')

                if to_value != 'None':

                    to_value = f"$milestone-{getattr(self.milestone, 'id', 'None')}"


                comment_text = f"changed milestone from {value} to {to_value}"

            elif field == 'planned_start_date':

                to_value = self._after[field]

                if to_value:

                    to_value = str(self._after[field].utcfromtimestamp(self._after[field].timestamp()))+ '+00:00'

                comment_text = f"changed Planned Start Date from _{self._before[field]}_ to **{to_value}**"

            elif field == 'planned_finish_date':

                to_value = self._after[field]

                if to_value:

                    to_value = str(self._after[field].utcfromtimestamp(self._after[field].timestamp()))+ '+00:00'

                comment_text = f"changed Planned Finish Date from _{self._before[field]}_ to **{to_value}**"

            elif field == 'real_start_date':

                to_value = self._after[field]

                if to_value:

                    to_value = str(self._after[field].utcfromtimestamp(self._after[field].timestamp()))+ '+00:00'

                comment_text = f"changed Real Start Date from _{self._before[field]}_ to **{to_value}**"

                to_value = self._after[field]

                if to_value:

                    to_value = str(self._after[field].utcfromtimestamp(self._after[field].timestamp()))+ '+00:00'

            elif field == 'real_finish_date':

                to_value = self._after[field]

                if to_value:

                    to_value = str(self._after[field].utcfromtimestamp(self._after[field].timestamp()))+ '+00:00'

                comment_text = f"changed Real Finish Date from _{self._before[field]}_ to **{to_value}**"


            elif field == 'description':

                comment_text = ''.join(
                    str(x) for x in list(
                        difflib.unified_diff(
                            str(self._before[field] + '\n').splitlines(keepends=True),
                            str(self._after[field] + '\n').splitlines(keepends=True),
                            fromfile = 'before',
                            tofile = 'after',
                            n = 10000,
                            lineterm = '\n'
                        )
                    )
                ) + ''

                comment_text = '<details><summary>Changed the Description</summary>\n\n``` diff \n\n' + comment_text + '\n\n```\n\n</details>'


            if (
                comment_text is None
                and field != 'created'
                and field != 'modified'
            ):

                raise centurion_exceptions.APIError(
                    detail = f'Action comment for field {field} will not be created. please report this as a bug.',
                    code = 'no_action_comment'
                )

            elif comment_text:

                if request:

                    if request.user.pk:

                        comment_user = request.user

                    else:

                        comment_user = None

                else:

                    comment_user = None

                # User requires entity to be usable for ticket comment
                # TicketCommentAction.objects.create(
                #     organization = self.organization,
                #     ticket = self,
                #     comment_type = TicketCommentAction._meta.sub_model_type,
                #     body = comment_text,
                #     # user = user
                # )

        # return None



    # def create_action_comment(self, user):

    #     from core.models.ticket_comment_action import TicketCommentAction

    #     comment = TicketCommentAction.objects.create(
    #         organization = self.organization,
    #         ticket = self.ticket,
    #         body = body,
    #         # user = user
    #     )


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        self._after = self.__dict__.copy()

        if self._before:

            self.create_action_comment()
