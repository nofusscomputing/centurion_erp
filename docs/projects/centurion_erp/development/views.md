---
title: Views
description: Views development Documentation for Centurion ERP
date: 2024-07-12
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Viewsets are used by Centurion ERP for each of the API views.


## Requirements

- Views are class based

- **ALL** views are `ViewSets`

- Views are saved within the module the model is from under path `viewsets/`

- views are documented at the class level for the swagger UI.

- Index Viewsets must be tested against tests `from api.tests.abstract.viewsets import ViewSetCommon`

- Model VieSets must be tested against the following tests:

    - _Unit Test Cases_ `app/api/tests/unit/test_unit_common_viewset.py`

        Within this file you'll find test cases that are suffixed with `InheritedCases`. The test case you should use is the one thats name begins with the class you inherited. for example, if the viewset inherits common ViewSet base class `ModelViewSet`, the class name of the pre-written test cases would be `ModelViewSetInheritedCases`.

    - _Functional test cases_ `from api.tests.abstract.api_serializer_viewset import SerializersTestCases`

    - _Functional test cases_ `from api.tests.abstract.api_permissions_viewset import APIPermission`

    - _Functional test cases_ (Only required if model has an API endpoint)_`from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional`

    - _Functional test cases_ _(Only required if model has nav menu entry)_`from api.tests.abstract.test_metadata_functional import MetaDataNavigationEntriesFunctional`

- View Added to Navigation

- ViewSets that are used to expose data that is publicly available **must** have it's filename prefixed with `public_`


## Creating a ViewSet

All ViewSets are to be saved under the django app they belong to and within a directory called `viewsets`. Serializers are broken down to match the [model types](./models.md#creating-a-model):


### Standard Model ViewSet


<!-- markdownlint-disable -->
#### Requirements
<!-- markdownlint-restore -->

- Inherits from one of the following base class':

    - Index ViewSet `api.viewsets.common.CommonViewSet`

    - Model ViewSet that are to be Read-Only `api.viewsets.common.ReadOnlyModelViewSet`

    - If not any of the above, `api.viewsets.common.ModelViewSet`


### Sub-Model ViewSet

Unless you are creating a new base sub-model, you will not need to create a ViewSet. This is because the sub-model Viewset that is used is the lowest base model in the inheritance chain.


<!-- markdownlint-disable -->
#### Requirements
<!-- markdownlint-restore -->

- Attribute 'base_model' must be specified within the ViewSet

- ViewSet must inherit from `api.viewsets.common.SubModelViewSet`

- Tested against:

    - Unit Tests:

        - `api.tests.unit.test_unit_common_viewset.SubModelViewSetInheritedCases`


## Permissions

If you wish to deviate from the standard CRUD permissions, define a function called `get_dynamic_permissions` within the `view`/`ViewSet`. The function must return a list of permissions. This is useful if you have added additional permissions to a model.

Example of the function `get_dynamic_permissions`

``` py

def get_dynamic_permissions(self):

    if self.action == 'create':

        self.permission_required = [
            'core.random_permission_name',
        ]

    else:

        raise ValueError('unable to determine the action_keyword')

    return super().get_permission_required()

```


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
