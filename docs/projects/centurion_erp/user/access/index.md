---
title: Access
description: Access Module Documentation for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

The Access module provides the multi-tenancy for this application. Tenancy is organized into tenants, which contain teams which contain users. As part of this module, application permission checking is also conducted.


## Components

- [Contact / Corporate Directory](./contact.md)

- [Tenant](./tenant.md)

- [Roles](./role.md)

- [Team](./team.md)


## Permission System

The permission system within Centurion ERP is custom and built upon Django's core permission types: add, change, delete and view. For a user to be granted access to perform an action, they must be assigned the permission and have that permission assigned to them as part of the tenant they are performing the action in. ALL assigned permissions are limited to the tenant the permission is assigned.

!!! tip
    User `A` is in tenant `A` and has device view permission. User `A` can view devices in Organization `A` **ONLY**. User `A` although they have the device view permission, can **not** view devices in tenant `B`. For User `A` to view devices in tenant `B` they would also require the device view permission be assigned to them within tenant `B`.

Unlike filesystem based permssions, Centurion ERP permissions are not inclusive, they are mutually exclusive. That is:

- To `add` an item you must have its corresponding `add` permission

- To `change` an item you must have its corresponding `change` permission

- To `delete` an item you must have its corresponding `delete` permission

- To `view` an item you must have its corresponding `view` permission

The exclusitvity is that each of the permissions listed above, dont include an assumed permission. For instance if you have the `add` permission for an item, you will not be able to view it. That would require the `view` permission.


### Gloabl Organization

If the webmaster has setup Centurion ERP to have a [global tenant](../settings/app_settings.md#global-tenant), as long as the user has the a `view` permission for the model in question in **any** tenant, they will be able to view that item within the global tenant. This is not the same for the other permissions: `add`, `change` and `delete`. To which they must be granted those permissions within the global tenant exclusively.

!!! tip
    User `A` is in tenant `A` and the webmaster has setup Centurion to use tenant `B` as the global tenant. If user `A` has been granted permission `itam.view_software` in tenant `A` they will be able to view software within both tenant `A` and `B`.
