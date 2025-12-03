---
title: Permissions
description: Permissions development Documentation for Centurion ERP
date: 2025-12-02
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

As Centurion ERP is multi-tenancy the permissions system has been designed to cater for this. Both model and object permissions are checked based of off the standard CRUD permissions, being `add`, `change`, `delete` and `view`. In addition the user must have the correct permission within the tenancy they are interacting with.

All available permissions classes within Centurion ERP are:

- `api.permissions.common.CenturionModelPermissions`

- `api.permissions.common.CenturionObjectPermissions`

- `access.permissions.tenancy.TenancyPermissions`

- `access.permissions.super_user.SuperUserPermissions`

- `access.permissions.user.UserPermissions`


## Requirements

All Permission Classes must meet the following requirements:

- function `has_object_permission` **must** return `bool` value

- function `has_permission` **must** return `bool` value

- No uncaught exception to be raised from any function/method within the permission class

- No Merge request that contains a permissions class will be merged unless the permissions class is [tested](./testing.md). This includes **all** branches.


## Centurion Model Permissions

This permission class a base class and should not be required on its own.


## Centurion Object Permissions

This permission class a base class and should not be required on its own. This class also inherits from `CenturionModelPermissions`.


## Tenancy Permissions

!!! info "TL;DR"
    Normally you will just inherit from a common ViewSet, however if required the mixin is -> `from app.access.mixins.tenancy include TenancyMixin`

A part from ensuring that your models have the [tenancy field](../user/access/tenant.md). There may be a requirement to check the tenancy of a parent model. As an example adding a comment to a model. When creating the comment (its own model), the tenancy may not be known. In the same token, the comment obtains its tenancy from the model. In this case within the ViewSet, ensure that the `parent_model` is set to that of the model, in this example the comment is being made on.

for example:

``` py

class MyViewSet(
    # The Common ViewSet to inherit from
):

    model = MyCommentModel

    parent_model = MyModel

```

Now when a comment is made, the permission system will fetch the tenancy from `parent_model = MyModel` to use to check if the user has the required permissions within that tenancy.

Additionally You may wish to ensure that a user has the parent model permissions alongsie the models permissions. To do this add the following to the view set class.

``` py

class MyViewSet(
    # The Common ViewSet to inherit from
):

    perms_map: dict[str, list[str]] = {
        'GET': [ parent_permission ],
        'OPTIONS': [ parent_permission ],
        'HEAD': [ parent_permission ],
        'POST': [ parent_permission ],
        'PUT': [ parent_permission ],
        'PATCH': [ parent_permission ],
        'DELETE': [ parent_permission ],
    }

```

By adding dictionary `perms_map`, the list of permissions next to the HTTP method that is being made for the request is added as an additional permission that the user must have.

!!! note
    Dict `perms_map` is only usable within permission class `api.permissions.common.CenturionModelPermissions`. This includes `api.permissions.common.CenturionObjectPermissions` and `access.permissions.tenancy.TenancyPermissions` as they inherit from it.


## Super User Permissions

As the name implies, this permission class allows access to the model/object if the user is a super-user.


## User Permissions

This permissions class checks the user field of the model in question. On finding that the authenticated user and the user field match, the user is granted acccess. This permission class does not care about the action being performed.
