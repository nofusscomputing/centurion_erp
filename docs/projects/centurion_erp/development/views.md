---
title: ViewsSets
description: ViewsSet development Documentation for Centurion ERP
date: 2024-07-12
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

A view within Centurion ERP are the objects that are both the ingress and egress of data in relation to the user. As Centurion ERP is an API application, we use specifically use ViewSets as our type of view.

There are many viewsets available within Centurion. Our viewsets are setup based off of the authorization the user should have, they are:

- `tenancy.py` Tenancy based objects

    Filter objects to and only allow access based off of the users tenancy.

- `user.py` User based objects

    Filter objects to and only allow access to the current authenticated user.

- `super_user.py` Super User objects

    Only allows access to a user whom has super user access.

- `public` Anonymous / Public User

    Unauthenticated users can access.

The authorization based viewsets can be located at path `app/api/viewsets/common/`

Within each authorization based viewset, the viewsets are further broken down into viewsets based off of features. i.e. Can view, can edit etc. These are derived from the common viewset (`common.py`) classes.


## Requirements

When working with viewsets the following requirements must be met:

- Views are class based

- **ALL** views are `ViewSets`

- Views are saved within the module the model is from under path `viewsets/`

- views are documented at the class level for the swagger UI.

- ViewSets must be tested both unit and functional:

    - _Unit Test Cases_ `app/api/tests/unit/test_unit_common_viewset.py` and `app/api/tests/unit/viewset/`

        Within this file you'll find test cases that are suffixed with `InheritedCases`. The test case you should use is the one thats name begins with the class you inherited. for example, if the viewset inherits common ViewSet base class `ModelViewSet`, the class name of the pre-written test cases would be `ModelViewSetInheritedCases`.

    - _Functional test cases_ `app/api/tests/functional/test_functional_common_viewset.py` and `app/api/tests/functional/viewset/`

- View Added to Navigation `app/api/react_ui_metadata.py`

- ViewSets that are used to expose data that is publicly available **must** have it's filename prefixed with `public_`

- No viewset inherits from the common viewset classes. ONLY inherit from the permission bassed classes.


## Permissions

Within Centurion ERP viewsets will normally user the [Tenancy Permissions](./permissions.md#tenancy-permissions) Mixin. To see more about the other available permission classes refer to its [docs](./permissions.md).


## Navigation

Although Centurion ERP is a Rest API application, there is a UI. The UI uses data from Centurion's API to render the view that the end user sees. One of those items is the navigation structure.

Location of the navigation is in `app/api/react_ui_metadata.py` under the attribute `_nav`.


### Menu Entry

When adding a view, that is also meant to be seen by the end user, a navigation entry must be added to the correct navgation menu. The entry is a python dictionary and has the following format.

``` pyhton

{
    '<app name>.<permission name>': {
        "display_name": "<menu entry name>",
        "name": "<html id>",
        "icon": "<menu entry icon>",
        "link": "<relative url.>"
    }
}

```

- `app name` _Optional_ is the centurion application name the model belongs to. This entry should only be supplied if the application name for the entry does not match the application for the [navigation menu](#menu).

- `permission name` is the centurion permission required for this menu entry to be rendered for the end user.

- `display_name` Menu entry name that the end user will see

- `name` This is used as part of the html rendering of the page. **must be unique** across ALL menu entries

- `icon` _Optional_ if specified, this is the name of the icon that the UI will place next to the menu entry. If this is not specified, the name key is used as the icon name.

- `link` the relative URL for the entry. this will be the relative URL of the API after the API's version number. _i.e. `/api/v2/assistance/ticket/request` would become `/assistance/ticket/request`_

Testing of the navigation is via `api.tests.unit.test_navigation_menu.py` If the item has a navigation menu entry the `setUpTestData` will need to be updated, along with test cases for the entry.


### Menu

The navigation menu is obtained by the UI as part of the metadata. The structure of the menu is a python dictionary in the following format:

``` python

 {
        '<app name>': {
            "display_name": "<Menu entry>",
            "name": "<menu id>",
            "pages": {
                '<menu entries>'
            }
        }
 }

```

- `app name` the centurion application name the menu belongs to.

- `display_name` Menu name that the end user will see

- `name` This is used as part of the html rendering of the page. **must be unique** across ALL menu entries

- `pages` [Menu entry](#menu-entry) dictionaries.

Upon the UI requesting the navigation menu, the users permission are obtained, and if they have the permission for the menu entry within **any** organization, they will be presented with the menu that has a menu entries.


## Testing

As per the requirements listed above, viewsets must be tested. Although most if not all test cases are already written, if the view you create is different; You must write the test case(s) for this difference.
