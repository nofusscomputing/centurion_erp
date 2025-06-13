---
title: Models
description: Centurion ERP Models development documentation
date: 2024-07-14
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Models within Centurion ERP are how the data is structured within the database. This page contains documentation pertinent to the development of the models for use with Centurion ERP.


## Creating a Model

All models are class based models. Due to this fact, most of the work has been done for the models. We have two types of models: normal and sub-model. In most cases to create a model you will only need to declare the fields and any validation.

When designing or even implementing a model do consider that what is defined within its class must take into account that the model is responsible for ensure that no data is saved to the database wherein it could create an inconsistancy. For ensureing this does not see [Validation](#validation-methods) below.


### Requirements

When creating models they must meet the following requirements:

- inherits from [`core.models.centurion.CenturionModel`](./api/models/centurion.md) or if a submodel `core.models.centurion.CenturionSubModel` and its base model.

- class has  the folloing objects defined:

    - Function `__str__` is defined to return the models name when requested as a string.

    - Attribute `page_layout` is defined with the models UI page layout

    - Attribute `table_fields` is defined with the fields to display by default for viewing the model within a table.


- Fields are initialized with the following parameters:

    - `verbose_name`

    - `help_text`

- contains a `Meta` sub-class with following attributes:

    - `ordering` _Order the results are returned in._

    - `verbose_name` _Name of the Model._

    - `verbose_name_plural` _Plural Name of the model_

- No `queryset` is to return data that the user has not got access to.

- Model Exceptions must be from `django.core.exceptions`

!!! tip
    It's a good idea to create the initial model class, then create and add the model tests for that class. This way you can run the tests to ensure that the requirements are met. Of Note, the tests may not cover ALL of the requirements section, due diligence will need to be exercised.


### Normal (Base) Model

This model is nothing special and is the core model type that will be created. If this model is inherited by a sub-model its also referred to as a _"base model."_ Creating one is as simple as simple as declaring the class, inheriting from `core.models.centurion.CenturionModel` then adding your fields and [validation method(s)](#validation-methods).


#### Available Base models

The are already some base models within Centurion ERP that you can use to extend and/or add features to Centurion easier. They are:


- [Asset](./accounting/asset.md)

    - [ITAM Asset](./itam/it_asset.md)

        _A sub-model of Asset. Used by the ITAM module_

- [Entity](./core/entity.md)

    - Company

        _A sub-model of Entity. All business like entities_

    - Person

        _A sub-model of Entity. As the name implies, A person_

        - Contact

            _A sub-model of Person. Contains fields that are common to a contact_

- [Ticket](./core/ticket.md)

    _All Ticketing Models use this_

- [Ticket Comment](./core/ticket_comment.md)

    _All Ticket Comment Models use this_

All sub-models are intended to be extended and contain the core features for ALL models. This aids in extensibility and reduces the work required to add a model.

!!! tip
    Core features can be switched on and/or off for the model you are creating. Before doing so though, consider the reasons for doing so and do discuss with a maintainer. This discussion will be required to ensure that you are not unintentially removing a feature that is a **must** for a Centurion ERP model.


### Sub-Model

A Sub-model specifically inherits from a normal model with the purpose of using the base model fields (the common fields) and if required specifying its own fields. A sub-model provides an additional feature in that the data from the base model can now be based off of the permissions of the sub-model, not the base. THis model inherits from `core.models.centurion.CenturionSubModel` and its base model.


## Core Features

All models must contain the core features, being:

- [Audit History](./core/model_history.md)

    _Every change that occurs to a model is recorded_

- [Notes](./core/model_notes.md)

    _Adds the ability for a user to add comments to a model_

- KB Article linking

    _Enables linking a knowledge base article to a model_

- Model Tag

    _Enables the possibility within markdown fields to use its [tag](../user/core/markdown.md#model-reference--model-tag) to create a link to the model._


## Validation Methods

Within All of our models including when they are created via an [API serializer](./serializers.md), the models [validators](https://docs.djangoproject.com/en/5.1/ref/models/instances/#validating-objects) are called. The models validators are responsible for ensuring that no data goes into the database that may create an inconsistancy.

!!! example
    You have defined a model that has a user field that must always have a value. This model can be access via the API, in which the user field is auto-populated by object `request.user`. In the same token you have admin commands that uses this model.
    Now every time you use the admin command to create this model, it will fail validation due to there being no value for the user field. This is where the models validator methods come into play. defining method `clean()` within the model with the logic required to ensure that the user field has value for the user field ensures that the model now when used by the admin command is consistant and meets the intent of the models purpose.

Whilst most data that will use a model will be via an API Serializer, which in turn has its own validation. The models Validation is only to serve the purpose of ensuring data consistancy.


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

The `table_fields` attribute within a model is what the UI List View or section table uses as the fields to add to the table. The `table_fields` attribute is a python list of string/dictionary that are the field names as are defined within the serializer. If the field is defined as a dictionary, the field is formatted as per the definition. for example:

``` py

table_fields: list = [
    'organization',
    'name'
    {
        'field': 'display_name',    # String, Name of the field to use
        'type': 'link',             # Choice, (link = anchor link) definition type
        'key': '_self'              # String, Dictionary key to use, in case of link. in this case will expand to `_urls._self`
    },
    'created'
]

```


## Depreciated Docs undergoing re-write

- ToDo

    - Avoid:

        - adding `model.delete()` method

        - adding `model.save()` method

    - Do

        - Add `model.clean()` To set/modify any field values, _if required_


<!-- markdownlint-disable -->
## Requirements
<!-- markdownlint-restore -->

- `clean()` method within a model is **only** used to ensure that the data entered into the DB is valid and/or to ensure application wide changes/validation is conducted prior to saving model.

- Tenancy models must have the ability to have a [knowledge base article](#knowledge-base-article-linking) linked to it.

- Models must save audit history


<!-- markdownlint-disable -->
#### Requirements
<!-- markdownlint-restore -->

- Must **not** be an abstract class

- Attribute `sub_model_type` must be specified within the models `Meta` sub-class

- File name is `<base model>_<sub_model_type>` where `base model` is the value of `Meta.sub_model_type` or the first model in the chain.


## Checklist

This section details the additional items that may need to be done when adding a new model:

- If the model is a primary model, add it to model reference rendering in `app/core/lib/markdown_plugins/model_reference.py` function `tag_html`

- If the model is a primary model, add it to the model link slash command in `app/core/lib/slash_commands/linked_model.py` function `command_linked_model`


## History

Adding [History](./core/model_history.md) to a model is automatic. If there is a desire not to have model history it can be disabled by adding attribute `_audit_enabled` to the model class and setting its value to `False.`


## Tests

The following Unit test suites exists for models:

- Unit Tests

    - model (Base Model) `core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model.CenturionAbstractModelInheritedCases`

    - model (Sub-Model) `core.tests.unit.centurion_sub_abstract.test_unit_centurion_sub_abstract_model.CenturionSubAbstractModelInheritedCases`


- Functional Tests

    - model `core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model.CenturionAbstractModelInheritedCases`

    - API Fields Render `api.tests.functional.test_functional_api_fields.APIFieldsInheritedCases`

!!! info
    If you add a feature you will have to [write the test cases](./testing.md) for that feature if they are not covered by existing test cases.

Each model has the following Test Suites auto-magic created:

- API Permissions checks `api.tests.functional.test_functional_meta_permissions_api`

    _Checks the CRUD permissions against the models API endpoints_

- Audit History Model checks, `core.tests.unit.centurion_audit_meta.test_unit_meta_audit_history_model`

    _Confirms the model has a [`AuditHistory`](./api/models/audit_history.md) model and other checks as required for an `AuditHistory` model._

These auto-magic tests require no input and will be created on a model inheriting from [`CenturionModel`](./api/models/centurion.md) and run every time the tests are run.


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
