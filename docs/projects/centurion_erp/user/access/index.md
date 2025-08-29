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

- [Company](./company.md)

- [Tenant](./tenant.md)

- [Roles](./role.md)

- [Team](./team.md)


### Gloabl Organization

If the webmaster has setup Centurion ERP to have a [global tenant](../settings/app_settings.md#global-tenant), as long as the user has the a `view` permission for the model in question in **any** tenant, they will be able to view that item within the global tenant. This is not the same for the other permissions: `add`, `change` and `delete`. To which they must be granted those permissions within the global tenant exclusively.

!!! tip
    User `A` is in tenant `A` and the webmaster has setup Centurion to use tenant `B` as the global tenant. If user `A` has been granted permission `itam.view_software` in tenant `A` they will be able to view software within both tenant `A` and `B`.
