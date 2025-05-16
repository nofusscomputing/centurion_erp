from django.db.models import Q

from django.conf import settings

from access.models.team_user import TeamUsers

from core.forms.common import CommonModelForm

class TeamUsersForm(CommonModelForm):

    class Meta:
        model = TeamUsers
        fields = [
            'user',
            'manager',
        ]
