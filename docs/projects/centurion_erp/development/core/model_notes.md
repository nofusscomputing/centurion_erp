---
title: Model Notes
description: Centurion ERP Model Notes development documentation
date: 2025-02-09
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Model Notes are a core feature that is intended to be used as the base for enabling a model to have notes assosiated to it.


## Adding Notes to a Model

Most of the work has already been done, all that is required to add notes to a model is the creation of the following:

- Model

- Serializer

- Viewset


### Model

The model is a proxy model for `core.models.model_notes.ModelNotes`. This model requires a `models.ForeignKey` field named `model` to the model that will be receinving the notes.


#### Example model

This example is for adding notes to the Manufacturer Model

``` py title="models/manufacturer_notes.py"

--8<-- "app/core/models/manufacturer_notes.py"

```


### Serializer

The Serializer contains the items the parent serializer (`core.serializers.model_notes`) does not have. This serializer requires the standard serializers be created that **ALL** inherit from the model notes parent serializer.


#### Example Serializer

This example is for adding notes to the Manufacturer Model

``` py title="serializers/manufacturer_notes.py"

--8<-- "app/core/serializers/manufacturer_notes.py"

```


### ViewSet

The ViewSet is a class that inherits from the Model Notes base ViewSet class, `core.viewsets.model_notes.ViewSet`. The ViewSet is responsible for providing the Serializer, Documentation (Swagger UI) and Providing the Model.


#### Example ViewSet

This example is for adding notes to the Manufacturer Model

``` py title="viewsets/manufacturer_notes.py"

--8<-- "app/core/viewsets/manufacturer_notes.py"

```


## Testing

As with any other object within Centurion, the addition of a feature requires it be tested. The following Test Suites are available:

- `Unit`

    - model - `core.tests.unit.model_notes.test_unit_model_notes.ModelNotesInheritedCases`

    - Serializer - `core.tests.abstract.test_unit_model_notes_serializer.ModelNotesSerializerTestCases`

    - Viewset - `api.tests.abstract.viewsets`

- `Functional`

    - ViewSet - `core.tests.abstract.test_functional_notes_viewset`

    - API fields render - `core.tests.abstract.model_notes_api_fields`
