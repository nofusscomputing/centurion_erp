from django import forms
from django.db.models import Q

from app import settings

from core.forms.common import CommonModelForm
from core.forms.validate_ticket_comment import TicketCommentValidation

from core.models.ticket.ticket_comment import TicketComment



class CommentForm(
    CommonModelForm,
    TicketCommentValidation
):

    prefix = 'ticket'

    class Meta:
        model = TicketComment
        fields = '__all__'


    def __init__(self, request, *args, **kwargs):

        self.request = request

        super().__init__(*args, **kwargs)

        self._ticket_organization = self.fields['ticket'].queryset.model.objects.get(pk=int(self.initial['ticket'])).organization

        self._ticket_type = kwargs['initial']['type_ticket']

        if 'qs_comment_type' in kwargs['initial']:

            self._comment_type = kwargs['initial']['qs_comment_type']

        else:

            self._comment_type = str(self.instance.get_comment_type_display()).lower()

        self.ticket_comment_permissions


        self.fields['planned_start_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'format': "%Y-%m-%dT%H:%M"})
        self.fields['planned_start_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['planned_start_date'].format="%Y-%m-%dT%H:%M"

        self.fields['planned_finish_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['planned_finish_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['planned_finish_date'].format="%Y-%m-%dT%H:%M"

        self.fields['real_start_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['real_start_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['real_start_date'].format="%Y-%m-%dT%H:%M"

        self.fields['real_finish_date'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['real_finish_date'].input_formats = settings.DATETIME_FORMAT
        self.fields['real_finish_date'].format="%Y-%m-%dT%H:%M"

        self.fields['body'].widget.attrs = {'style': "height: 800px; width: 900px"}

        self.fields['duration'].widget = self.fields['duration'].hidden_widget()

        self.fields['user'].initial = kwargs['user'].pk
        self.fields['user'].widget = self.fields['user'].hidden_widget()

        self.fields['ticket'].widget = self.fields['ticket'].hidden_widget()

        self.fields['parent'].widget = self.fields['parent'].hidden_widget()
        self.fields['comment_type'].widget = self.fields['comment_type'].hidden_widget()

        if not( self._has_import_permission or self._has_triage_permission or request.user.is_superuser ):

            self.fields['source'].initial = TicketComment.CommentSource.HELPDESK

            self.fields['source'].widget = self.fields['source'].hidden_widget()

        else:

            self.fields['source'].initial = TicketComment.CommentSource.DIRECT




        if self._comment_type == 'task':

            self.fields['comment_type'].initial = self.Meta.model.CommentType.TASK

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                task = True
            )

        elif self._comment_type == 'comment':

            self.fields['comment_type'].initial = self.Meta.model.CommentType.COMMENT

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                comment = True
            )

        elif self._comment_type == 'solution':

            self.fields['comment_type'].initial = self.Meta.model.CommentType.SOLUTION

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                solution = True
            )

        elif self._comment_type == 'notification':

            self.fields['comment_type'].initial = self.Meta.model.CommentType.NOTIFICATION

            self.fields['category'].queryset = self.fields['category'].queryset.filter(
                notification = True
            )


        allowed_fields = self.fields_allowed

        original_fields = self.fields.copy()


        for field in original_fields:

            if field not in allowed_fields and not self.fields[field].widget.is_hidden:

                del self.fields[field]


    def clean(self):
        
        cleaned_data = super().clean()

        return cleaned_data

    def is_valid(self) -> bool:

        is_valid = super().is_valid()

        validate_ticket_comment: bool = self.validate_ticket_comment()

        if not validate_ticket_comment:

            is_valid = validate_ticket_comment

        return is_valid



class DetailForm(CommentForm):

    prefix = 'ticket'

    class Meta:
        model = TicketComment
        fields = '__all__'


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
