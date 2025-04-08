from django.contrib import admin

from settings.models.app_settings import AppSettings



class AppSettingsAdmin(admin.ModelAdmin):

    fieldsets = [
        ( None,
            {
                "fields": [
                    "owner_organization",
                    'global_organization',
                    'created',
                    'modified',
                ]
            }
        ),
        ('Settings',
            {
                "fields": [
                    "device_model_is_global",
                    'device_type_is_global',
                    "manufacturer_is_global",
                    'software_is_global',
                    'software_categories_is_global'
                ]
            }
        ),
    ]


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['owner_organization', 'created', 'modified' ]
        else:
            return []


    def has_add_permission(self, request):    # Hide `Add` button when one item exists
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):    # Hide `Delete` Button
        return False



admin.site.register(AppSettings,AppSettingsAdmin)
