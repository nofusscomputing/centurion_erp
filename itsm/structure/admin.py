from django.contrib import admin

from organizations.models import (Organization, OrganizationUser,
    OrganizationOwner, OrganizationInvitation)

admin.site.unregister(Organization)
admin.site.unregister(OrganizationInvitation)
admin.site.unregister(OrganizationOwner)

from .models import Organization, Team


class TeamInline(admin.TabularInline):
    model = Team
    extra = 1

    fk_name = 'organization'


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Date information", {"fields": ["slug"], "classes": ["collapse"]}),
    ]
    inlines = [TeamInline]
    list_display = ["name", "created", "modified"]
    list_filter = ["created"]
    search_fields = ["name"]


admin.site.register(Organization,OrganizationAdmin)
