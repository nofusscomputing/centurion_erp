from django.db.models import Q

from app import settings

from access.models.team_user import TeamUsers

from core.forms.common import CommonModelForm

class TeamUsersForm(CommonModelForm):

    class Meta:
        model = TeamUsers
        fields = [
            'user',
            'manager',
        ]
