import json

from django.db.models import Q
from django.shortcuts import render
from django.template import Template, Context
from django.views import generic

from access.mixin import OrganizationPermission

from core.views.common import DisplayView

class Index(DisplayView):

    # permission_required = [
    #     'itil.view_knowledge_base'
    # ]

    template_name = 'form.html.j2'


    def get(self, request):
        context = {}

        user_string = Template("{% include 'icons/issue_link.html.j2' with issue=10 %}")
        user_context = Context(context)
        context['form'] = user_string.render(user_context)


        context['content_title'] = 'Knowledge Base'

        return render(request, self.template_name, context)
