import django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from access.models.tenant import Tenant as Organization
from access.models.role import Role



class RoleGroupsInline(admin.TabularInline):
    model = Role.groups.through
    extra = 0

    fields = ['group']

    fk_name = 'role'

    verbose_name = "Group"
    verbose_name_plural = "Groups"



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    inlines = [RoleGroupsInline]
    fields = ['name', 'organization', 'created', 'modified']  #
    readonly_fields = [ 'name', 'created', 'modified' ]



class OrganizationRoleInline(admin.TabularInline):
    model = Role
    extra = 0

    fields = [ 'name' ]

    fk_name = 'organization'



@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", 'manager']}),
    ]
    inlines = [OrganizationRoleInline]
    list_display = ["name", "created", "modified"]
    list_filter = ["created"]
    search_fields = ["role"]



class RoleUsersInline(admin.TabularInline):
    model = Role.users.through
    fk_name = "centurionuser"
    extra = 0

    fields = ['centurionuser', 'role' ]

    verbose_name = "Role"
    verbose_name_plural = "Roles"



class UsrAdmin(UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                ),
            },
        ),
    )

    inlines = [RoleUsersInline]

admin.site.register(django.contrib.auth.get_user_model(),UsrAdmin)
