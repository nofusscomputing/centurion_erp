from django.http import Http404
from django.urls import reverse
from django.views import generic

from django_celery_results.models import TaskResult

from access.mixin import OrganizationPermission

from core.forms.ticket import DetailForm, TicketForm
from core.models.ticket.ticket import Ticket
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = TicketForm

    model = Ticket


    def get_dynamic_permissions(self):

        return [
            str('core.add_ticket_' + self.kwargs['ticket_type']),
        ]


    def get_initial(self):

        initial = super().get_initial()

        initial.update({
            'type_ticket': self.kwargs['ticket_type'],
        })

        if self.kwargs['ticket_type'] == 'project_task':

            initial.update({
                'project': int(self.kwargs['project_id'])
            })

        return initial


    def form_valid(self, form):

        created: bool = False

        if form.instance.id is None:

            created = True

        val = super().form_valid(form)

        if created:

            form.instance.subscribed_users.add(form.instance.opened_by)

        return val



    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def get_success_url(self, **kwargs):

        if self.kwargs['ticket_type'] == 'request':

            return reverse('Assistance:_ticket_request_view', args=(self.kwargs['ticket_type'],self.object.id,))

        elif self.kwargs['ticket_type'] == 'project_task':

            return reverse('Project Management:_project_task_view', args=(self.kwargs['project_id'], self.kwargs['ticket_type'],self.object.id,))

        else:

            return reverse('ITIM:_ticket_' + str(self.kwargs['ticket_type']).lower() + '_view', args=(self.kwargs['ticket_type'],self.object.id,))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Ticket'

        return context



class Change(ChangeView):

    form_class = TicketForm

    model = Ticket


    def get_dynamic_permissions(self):

        return [
            str('core.change_ticket_' + self.kwargs['ticket_type']),
        ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = str(self.object)

        return context


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def get_initial(self):

        initial = super().get_initial()

        initial.update({
            'type_ticket': self.kwargs['ticket_type'],
        })

        if self.kwargs['ticket_type'] == 'project_task':

            initial.update({
                'project': int(self.kwargs['project_id'])
            })

        return initial


    def get_success_url(self, **kwargs):

        if self.kwargs['ticket_type'] == 'request':

            return reverse('Assistance:_ticket_request_view', args=(self.kwargs['ticket_type'],self.object.id,))

        elif self.kwargs['ticket_type'] == 'project_task':

            return reverse('Project Management:_project_task_view', args=(self.kwargs['project_id'], self.kwargs['ticket_type'],self.object.id,))

        else:

            return reverse('ITIM:_ticket_' + str(self.kwargs['ticket_type']).lower() + '_view', args=(self.kwargs['ticket_type'],self.object.id,))


class Delete(DeleteView):

    model = Ticket


    def get_dynamic_permissions(self):

        return [
            str('core.delete_ticket_' + self.kwargs['ticket_type']),
        ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + str(self.object)

        return context


    def get_success_url(self, **kwargs):

        if self.kwargs['ticket_type'] == 'request':

            return reverse('Assistance:Requests')
        
        elif self.kwargs['ticket_type'] == 'project_task':

            return reverse('Project Management:_project_view', kwargs={'pk': self.object.id})

        else:

            if self.kwargs['ticket_type'] == 'change':
                path = 'Changes'

            elif self.kwargs['ticket_type'] == 'incident':
                path = 'Incidents'

            elif self.kwargs['ticket_type'] == 'problem':
                path = 'Problems'


            return reverse('ITIM:' + path)



class Index(OrganizationPermission, generic.ListView):

    context_object_name = "tickets"

    fields = [
        "id",
        'title',
        'status',
        'date_created',
    ]

    model = Ticket

    template_name = 'core/ticket/index.html.j2'


    def get_dynamic_permissions(self):

        return [
            str('core.view_ticket_' + self.kwargs['ticket_type']),
        ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs['ticket_type'] == 'request':

            context['new_ticket_url'] = reverse('Assistance:_ticket_request_add', args=(self.kwargs['ticket_type'],))

        else:
            
            context['new_ticket_url'] = reverse(str('ITIM:_ticket_' + self.kwargs['ticket_type'] + '_add'), args=(self.kwargs['ticket_type'],))


        context['ticket_type'] = self.kwargs['ticket_type']

        context['content_title'] = 'Tickets'

        return context


    def get_queryset(self):

        if not hasattr(Ticket.TicketType, str(self.kwargs['ticket_type']).upper()):
            raise Http404

        queryset = super().get_queryset()

        queryset = queryset.filter(
            ticket_type = Ticket.TicketType[str(self.kwargs['ticket_type']).upper()]
        )

        return queryset


    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_model_view', args=(self.kwargs['pk'],))



class View(ChangeView):

    model = Ticket

    template_name = 'core/ticket.html.j2'

    form_class = DetailForm

    context_object_name = "ticket"


    def get_dynamic_permissions(self):

        return [
            str('core.view_ticket_' + self.kwargs['ticket_type']),
        ]



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        context['ticket_type'] = self.kwargs['ticket_type']

        url_kwargs = { 'ticket_type': self.kwargs['ticket_type'], 'pk': self.kwargs['pk']}

        if self.kwargs['ticket_type'] == 'request':

            path = 'Assistance:_ticket_request_change'

            context['model_delete_url'] = reverse('Assistance:_ticket_' + self.kwargs['ticket_type'] + '_delete', kwargs=url_kwargs)

        elif self.kwargs['ticket_type'] == 'project_task':

            path = 'Project Management:_project_task_change'

            url_kwargs = { 'project_id': self.kwargs['project_id'],'ticket_type': self.kwargs['ticket_type'], 'pk': self.kwargs['pk']}

            context['model_delete_url'] = reverse('Project Management:_project_task_delete', kwargs=url_kwargs)

        else:

            comment_path = 'ITIM:_ticket_comment_' + self.kwargs['ticket_type']

            if self.kwargs['ticket_type'] == 'change':

                path = 'ITIM:_ticket_change_change'

            elif self.kwargs['ticket_type'] == 'incident':

                path = 'ITIM:_ticket_incident_change'

            elif self.kwargs['ticket_type'] == 'problem':

                path = 'ITIM:_ticket_problem_change'


            context['model_delete_url'] = reverse('ITIM:_ticket_' + self.kwargs['ticket_type'] + '_delete', kwargs=url_kwargs)

        context['edit_url'] = reverse(
            path,
            kwargs = url_kwargs,
        ) # /assistance/ticket/{{ ticket_type }}/{{ ticket.id }}


        context['content_title'] = self.object.title

        return context


    def get_initial(self):
        return {
            'type_ticket': self.kwargs['ticket_type'],
        }
