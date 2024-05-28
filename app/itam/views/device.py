import json
import markdown

# from django.contrib.auth.decorators import permission_required
from django.contrib.auth import decorators as auth_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from access.mixin import OrganizationPermission
from access.models import Organization

from ..models.device import Device, DeviceSoftware, DeviceOperatingSystem
from ..models.software import Software

from core.forms.comment import AddNoteForm
from core.models.notes import Notes

from itam.forms.device_softwareadd import SoftwareAdd
from itam.forms.device_softwareupdate import SoftwareUpdate

from itam.forms.device.device import DeviceForm
from itam.forms.device.operating_system import Update as OperatingSystemForm

from settings.models.user_settings import UserSettings

class IndexView(PermissionRequiredMixin, OrganizationPermission, generic.ListView):
    model = Device
    permission_required = 'itam.view_device'
    template_name = 'itam/device_index.html.j2'
    context_object_name = "devices"

    paginate_by = 10

    def get_queryset(self):

        if self.request.user.is_superuser:

            return Device.objects.filter().order_by('name')

        else:

            return Device.objects.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')



def _get_form(request, formcls, prefix, **kwargs):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix, **kwargs)

class View(OrganizationPermission, generic.UpdateView):

    model = Device

    permission_required = [
        'itam.view_device'
        'itam.change_device'
    ]

    template_name = 'itam/device.html.j2'

    form_class = DeviceForm

    context_object_name = "device"

    paginate_by = 10



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        try:
            operating_system_version = DeviceOperatingSystem.objects.get(device=self.kwargs['pk'])
        
        except DeviceOperatingSystem.DoesNotExist:

            operating_system_version = None

        if operating_system_version:

            context['operating_system'] = OperatingSystemForm(prefix='operating_system', instance=operating_system_version)

        else:

            context['operating_system'] = OperatingSystemForm(prefix='operating_system')


        softwares = DeviceSoftware.objects.filter(device=self.kwargs['pk'])[:50]
        context['installed_software'] = len(DeviceSoftware.objects.filter(device=self.kwargs['pk']))

        context['softwares'] = softwares

        context['notes_form'] = AddNoteForm(prefix='note')

        context['notes'] = Notes.objects.filter(device=self.kwargs['pk'])

        config = self.object.get_configuration(self.kwargs['pk'])
        context['config'] = json.dumps(config, indent=4, sort_keys=True)

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('ITAM:_device_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context

    @method_decorator(auth_decorator.permission_required("itam.change_device", raise_exception=True))
    def post(self, request, *args, **kwargs):

        device = Device.objects.get(pk=self.kwargs['pk'])

        try:

            existing_os = DeviceOperatingSystem.objects.get(device=self.kwargs['pk'])

        except DeviceOperatingSystem.DoesNotExist:

            existing_os = None

        operating_system = OperatingSystemForm(request.POST, prefix='operating_system', instance=existing_os)

        if operating_system.is_bound and operating_system.is_valid():

            operating_system.instance.organization = device.organization
            operating_system.instance.device = device

            operating_system.save()


        notes = AddNoteForm(request.POST, prefix='note')

        if notes.is_bound and notes.is_valid() and notes.instance.note != '':

            notes.instance.organization = device.organization
            notes.instance.device = device
            notes.instance.usercreated = request.user

            notes.save()



        return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return f"/itam/device/{self.kwargs['pk']}/"



class SoftwareView(OrganizationPermission, generic.UpdateView):
    model = DeviceSoftware
    permission_required = [
        'itam.view_devicesoftware'
    ]
    template_name = 'form.html.j2'



    context_object_name = "devicesoftware"

    form_class = SoftwareUpdate


    def form_valid(self, form):
        device = Device.objects.get(pk=self.kwargs['device_id'])

        form.instance.organization_id = device.organization.id
        form.instance.device_id = self.kwargs['device_id']

        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return f"/itam/device/{self.kwargs['device_id']}/"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Edit Software Action'

        return context



class Add(OrganizationPermission, generic.CreateView):
    model = Device
    permission_required = [
        'itam.add_device',
    ]
    template_name = 'form.html.j2'
    fields = [
        'name',
        'serial_number',
        'uuid',
        'device_type',
        'organization',
    ]

    def get_initial(self):
        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }

    def form_valid(self, form):
        form.instance.is_global = False
        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return f"/itam/device/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Device'

        return context



class SoftwareAdd(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = DeviceSoftware
    permission_required = [
        'itam.add_devicesoftware',
    ]
    template_name = 'form.html.j2'
    # fields = [
    #     'software',
    #     'action'
    # ]

    form_class = SoftwareAdd


    def form_valid(self, form):
        device = Device.objects.get(pk=self.kwargs['pk'])
        form.instance.organization_id = device.organization.id
        form.instance.device_id = self.kwargs['pk']

        software = Software.objects.get(pk=form.instance.software.id)

        if DeviceSoftware.objects.get(device=device, software=software):


            software_version = DeviceSoftware.objects.get(
                device=device,
                software=software
            )

            software_version.action = form.instance.action
            software_version.save()

            return HttpResponseRedirect(self.get_success_url())
        
        else:

            return super().form_valid(form)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        device = Device.objects.get(pk=self.kwargs['pk'])
        kwargs['organizations'] = [ device.organization.id ]
        return kwargs


    def get_success_url(self, **kwargs):

        return f"/itam/device/{self.kwargs['pk']}/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Software Action'

        return context



class Delete(OrganizationPermission, generic.DeleteView):
    model = Device
    permission_required = [
        'itam.delete_device',
    ]
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return f"/itam/device/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
