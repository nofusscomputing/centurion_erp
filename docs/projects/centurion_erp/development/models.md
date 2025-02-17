---
title: Models
description: Centurion ERP Models development documentation
date: 2024-07-14
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Models within Centurion ERP are how the data is structured within the database. This page contains documentation pertinent to the development of the models for use with Centurion ERP.

All models within Centurion ERP are what we call a "Tenancy Object." A tenancy object is a model that takes advantage of the multi-tenancy features of Centurion ERP.


## Requirements

All models must meet the following requirements:

- inherits from [`app.access.models.TenancyObject`](./api/models/tenancy_object.md)

    !!! tip
        There is no requirement to include class [`app.core.mixin.history_save.SaveHistory`](./api/models/core_history_save.md) for inheritence as this class is already included within class [`app.access.models.TenancyObject`](./api/models/tenancy_object.md).

    !!! note
        If there is a specific use case for the object not to be a tenancy object, this will need to be discussed with a maintainer.

- class has `__str__` method defined to return that is used to return a default value if no field is specified.

- Fields are initialized with the following parameters:

    - `verbose_name`

    - `help_text`

- No `queryset` is to return data that the user has not got access to. _see [queryset()](./api/models/tenancy_object.md#tenancy-object-manager)_

- Single Field validation is conducted if required.

    !!! danger "Requirement"
        Multi-field validation, or validation that requires access to multiple fields must be done within the [form class](./forms.md#requirements).

- contains a `Meta` sub-class with following attributes:

    - `ordering` _Order the results are returned in._

    - `verbose_name` _Name of the Model._

    - `verbose_name_plural` _Plural Name of the model_

- If creating a new model, function `access.functions.permissions.permission_queryset()` has been updated to display the models permission(s)

- Attribute `page_layout` is defined with the models UI page layout

- Attribute `table_fields` is defined with the fields to display by default for viewing the model within a table.

- `clean()` method within a model is **only** used to ensure that the data entered into the DB is valid and/or to ensure application wide changes/validation is conducted prior to saving model.

- Tenancy models must have the ability to have a [knowledge base article](#knowledge-base-article-linking) linked to it.

- Models must save audit history


## Checklist

This section details the additional items that may need to be done when adding a new model:

- If the model is a primary model, add it to model reference rendering in `app/core/lib/markdown_plugins/model_reference.py` function `tag_html`

- If the model is a primary model, add it to the model link slash command in `app/core/lib/slash_commands/linked_model.py` function `command_linked_model`

!!! tip
    It's a good idea to create the initial model class, then create and add the model tests for that class. This way you can run the tests to ensure that the requirements are met. Of Note, the tests may not cover ALL of the requirements section, due diligence will need to be exercised.


## page_layout Attribute

Within the model attributes, `page_layout` is required. This attribute is what the UI uses to render the page. simply put, it's the layout of the page. Currently this layout is for a models details page only.

The `page_layout` attribute is a python list that is broken down into dictionaries for the page tabs, which then contain the page sections. Breakdown of the page layout is as follows:

- `Tab` These are the tabs at the top of a models details page. A tab contains sections.

- `Section` The page is broken down horizontially into sections. A section contains columns or a table.

- `Column` Vertical breakdown of a section. A column contains fields.

- `Table` A table is a layout for a section. The table renders a sub-model as part of the existing models information.

Example of ALL available options for the `page_layout` attribute.

``` python

page_layout: list = [
    {    # Detail Tab.
        "name": "Details",    # Tab name.
        "slug": "details",    # HTML id field.
        "sections": [    # Page Sections.
            {    # double column section.
                "layout": "double",
                "left": [    # Left column. This list is a list of fields that match the serializer fields.
                    'organization',
                    'name',
                    'is_global',
                ],
                "right": [    # right column. This list is a list of fields that match the serializer fields.
                    'model_notes',
                    'created',
                    'modified',
                ]
            },
            {    # Table Section.
                "layout": "table",
                "name": "Dependent Services",    # Heading for the section.
                "field": "service",    # field name within the `_urls` dict of the api query. which is where the data will be fetched from.
            },
            {    # single column section.
                "layout": "single",
                "fields": [    # This list is a list of fields that match the serializer fields.
                    'config',
                ]
            }
        ]
    },
    {    # Notes Tab.
        "name": "Notes",
        "slug": "notes",
        "sections": []    # The notes tab is a special case that requires no sections to be defined.
    },
] 

```


## table_fields Attributes

The `table_fields` attribute within a model is what the UI List View or section table uses as the fields to add to the table. The `table_fields` attribute is a python list of strings that are the field names as are defined within the serializer.


## History

Adding History to a model is a simple process. Please see the [Model History](./core/model_history.md) docs.


## Tests

The following Unit test cases exists for models:

- [BaseModel](./api/tests/models.md#base-unit-tests-for-all-models)

- [TenancyObject](./api/tests/models.md#tenancy-model-unit-tests)

!!! info
    If you add a feature you will have to write the test cases for that feature if they are not covered by existing test cases.


## Knowledge Base Article linking

All Tenancy Models must have the ability to be able to have a knowledge base article linked to it. To do so the following must be done:

- Add to the serializer as part of dictionary `_urls` key `knowledge_base` that resolves to the article url.

    ``` python

    def get_url(self, obj) -> dict:

        return {
            '_self': ...,
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
        }

    ```

- Add to the models `page_layout` attirubute a tab called `Knowledge Base`

    ``` python

    page_layout: dict = [
        {
            "name": "Knowledge Base",
            "slug": "kb_articles",
            "sections": [
                {
                    "layout": "table",
                    "field": "knowledge_base",
                }
            ]
        },
    ]

    ```


## Docs to clean up

!!! note
    The below documentation is still to be developed. As such what is written below may be incorrect.

for items that have a parent item, modification will need to be made to the mixin by adding the relevant check and setting the relevant keys.

``` python

if self._meta.model_name == 'deviceoperatingsystem':

    item_parent_pk = self.device.pk
    item_parent_class = self.device._meta.model_name

```
