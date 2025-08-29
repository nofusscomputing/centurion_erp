---
title: Authentication / Authorization
description: Authentication administration documentation for Centurion ERP by No Fuss Computing
date: 2024-07-19
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Centurion ERP authorization system is scoped to a single [tenancy](../user/access/tenant.md) and is role based ([RBAC](../user/access/role.md)). A user must be assigned the permission witin a tenancy to be able to perform the relevant action.

!!! info
    Permissions are mutually exclusive. That is, if a user has been granted an `add` permission, they will not be able to view the or any object as this requires the `view` permission. This is by design.


## Authentication

Centurion ERP requires that the user be authenticated to access its features. Within Centurion ERP there is the built-in authentication as well as Single Sign on (SSO) via an identity broker.

Centurion ERP also offers token authentication that obtains its permission from the token owner.


## Authorization

Authorization is done via [RBAC](../user/access/role.md) and is scoped to the tenancy the role is a part of. for configuring please see the [role](../user/access/role.md) documentation.
