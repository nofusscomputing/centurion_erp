---
title: Roles
description: Centurion ERP Roles for RBAC User documentation
date: 2025-04-07
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

A Role is used as part of authorization. This provides for a feature known as Role Base Access Control or RBAC for short. Roles are assigned permissions to conduct an action with the user or group being assigned a role. This in turn allows a user to conduct an action. By default no user has any permission to conduct any action. This means that once a user is assigned a role with a/many permission(s) they will be able to act according to the assigned permissions. If a user is assigned multiple roles, they will have the permissions of all roles combined.

!!! warning
    This feature is currently behind feature flag `2025-00003` and will remain so until roles are production ready. see [#551](https://github.com/nofusscomputing/centurion_erp/issues/551) for more details
