---
title: Roles
description: Centurion ERP Roles for RBAC User documentation
date: 2025-04-07
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

A Role is used as part of authorization. This provides for a feature known as Role Base Access Control or RBAC for short. Roles are assigned permissions to conduct an action with the user or group being assigned a role. This in turn allows a user to conduct an action. By default no user has any permission to conduct any action. This means that once a user is assigned a role with a/many permission(s) they will be able to act according to the assigned permissions. If a user is assigned multiple roles, they will have the permissions of all roles combined and have those permissions for the tenancy the role is a part of.


## Permission System

The permission system within Centurion ERP is custom and built upon Django's core permission types: add, change, delete and view. For a user to be granted access to perform an action, they must be assigned the permission. To do this create a role in the [tenancy](./tenant.md) that the permissions will be part of, assign permissions to that role and then assign the role to either the user or the group they are a part of.


!!! tip
    User `A` is in tenancy `A` and has device view permission. User `A` can view devices in tenancy `A` **ONLY**. User `A` although they have the device view permission, can **not** view devices in tenancy `B`. For User `A` to view devices in tenancy `B` they would also require the device view permission be assigned to them within tenancy `B`.

Unlike filesystem based permssions, Centurion ERP permissions are not inclusive, they are mutually exclusive. That is:

- To `add` an item you must have its corresponding `add` permission

- To `change` an item you must have its corresponding `change` permission

- To `delete` an item you must have its corresponding `delete` permission

- To `view` an item you must have its corresponding `view` permission

The exclusitvity is that each of the permissions listed above, dont include an assumed permission. For instance if you have the `add` permission for an item, you will not be able to view it. That would require the `view` permission.
