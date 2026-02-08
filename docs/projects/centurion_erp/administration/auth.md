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


### Single Sign On (SSO)

Single signon is provided by [python social auth](https://python-social-auth.readthedocs.io/en/latest/backends/index.html#social-backends) which provides support to authenticate against multiple different providers. Although many different providers can be configured, we develop and test against [Keycloak](https://www.keycloak.org/) as the provider.

To configure Keycloak as the SSO backend, Follow the [Guide](https://python-social-auth.readthedocs.io/en/latest/backends/keycloak.html) from the docs.


#### Limiting who can log in to Centurion

Centurion ERP has the abiltiy when using the keycloak backend to enforce which users are permitted to log in. This is done by ensuring that a claim is within the access token and has the defined value. To configure this add the following to Centurion's settings:

- `SOCIAL_AUTH_KEYCLOAK_REQUIRED_CLAIM_NAME`, _String_ - Name of the claim to check

- `SOCIAL_AUTH_KEYCLOAK_REQUIRED_CLAIM_VALUE`, _String_ - Value of the claim to check

!!! tip
    These config values are case sensitive. Not matching case will cause the checks to fail.

Once these Settings have been added, everytime a user logs in to Centurion ERP The users access token will be checked. If the claim name does not exist or the claim value is not what is defined, the user will not be able to log into Centurion.


##### Example

``` py

SOCIAL_AUTH_KEYCLOAK_REQUIRED_CLAIM_NAME = 'roles'
SOCIAL_AUTH_KEYCLOAK_REQUIRED_CLAIM_VALUE = 'User'

```

This example will check that a users access token contains a claim called `roles` and that within the roles, there is a value of `User`. On a match the login flow continues. On the inverse, the user will be denied access.


## Authorization

Authorization is done via [RBAC](../user/access/role.md) and is scoped to the tenancy the role is a part of. for configuring please see the [role](../user/access/role.md) documentation.
