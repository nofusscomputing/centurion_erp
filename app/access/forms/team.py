from django import forms
from django.db.models import Q
from django.forms import inlineformset_factory

from .team_users import TeamUsersForm, TeamUsers

from access.models.team import Team
from access.functions import permissions

from app import settings

from core.forms.common import CommonModelForm

TeamUserFormSet = inlineformset_factory(
    model=TeamUsers,
    parent_model= Team,
    extra = 1,
    fields=[
        'user',
        'manager'
    ]
)



class TeamFormAdd(CommonModelForm):

    class Meta:
        model = Team
        fields = [
            'team_name',
            'model_notes',
        ]



class TeamForm(CommonModelForm):

    class Meta:
        model = Team
        fields = [
            'team_name',
            'permissions',
            'model_notes',
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created'] = forms.DateTimeField(
            label="Created",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].created,
            disabled=True,
            required=False,
        )

        self.fields['modified'] = forms.DateTimeField(
            label="Modified",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].modified,
            disabled=True,
            required=False,
        )

        self.fields['permissions'].widget.attrs = {'style': "height: 200px;"}

        self.fields['permissions'].queryset = permissions.permission_queryset()
