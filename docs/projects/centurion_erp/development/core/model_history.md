---
title: Model History
description: Centurion ERP Model History development documentation
date: 2025-02-15
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Model History is a core feature that is intended to be used to keep an audit history of **ALL** changes to a model. All Tenancy Models are to have a history model created for it.


## Adding History to a Model

Most of the work has already been done, all that is required to add history to a model is the creation of the following:

- Model

- Function `get_serialized_model` added to audit model _(parent model only)_

- Function `get_serialized_child_model` added to audit model _(child model only)_

- _(child model only)_ model name added to list attribute in `core.models.model_history.ModelHistory.child_history_models`

    !!! tip
        To obtain the model name you can use the api at endpoint `api/v2/base/content_type` and then filtering by app_name and model. The value in the model field is what's required.


### Model

The model must inherit from `core.models.model_history.ModelHistory`. This model requires a `models.ForeignKey` field named `model` be added to the new history model that will be receiving the history feature. The foriegn key relationship is to the model that will be receiving the history. There is also a requirement to add a function called `get_serialized_model` that returns the serialized model, using the "base" serializer. The model that is serialized is the model the history is for,

As history can be broken up into parent-child relationships, if the model in question is a child model. The history model that will then be inherited from is the parent model history class. As this class will already contain the field `model`, the child history class must add field `child_model` which like the field `model` is also a `models.ForeignKey`.

Like the parent history model, A serializer is required. In this case the serializer function is to be called `get_serialized_child_model` that returns the serialized child model. Again like the parent history model using the "base" serializer. The model that is serialized is the child model the history is for,


#### Example model

This example is for adding history to the Device Model

``` py title="models/device_history.py"

--8<-- "app/itam/models/device_history.py"

```

This example is for adding history to the child model DeviceSoftware

``` py title="models/device_software_history.py"

--8<-- "app/itam/models/device_software_history.py"

```

!!! tip
    Take note of the inheritence and the fact that children don't override parent objects.

!!! danger "Requirement"
    Ensure that for the `model` and `child_model` fields that they are called with `related_name = history`. This ensures that **ALL** models that have history, will have an attribute called `history` that is available when working with that model.


## Audit Model

For history to save, there is a requirement to add a function to the model being audited. This function is to be called `save_history`. The sole purpose of this function is to call the super class (History class) function of the same name, although this time passing the history model.

Example of the required function, in this case for the `Device` model.

``` py


def save_history(self, before: dict, after: dict) -> bool:

    from itam.models.device_history import DeviceHistory

    history = super().save_history(
        before = before,
        after = after,
        history_model = DeviceHistory
    )

    return history

```


## Testing

As with any other object within Centurion, the addition of a feature requires it be tested. The following Test Suites are available:

- `Unit` - API Fields checks

    - `core.tests.abstract.test_unit_model_history_api_v2.PrimaryModelHistoryAPI` for parent / Primary history model

    - `core.tests.abstract.test_unit_model_history_api_v2.ChildModelHistoryAPI` for child history model

- `Functional` - History entry checks

    - `core.tests.abstract.test_functional_history.HistoryEntriesCommon` for parent / Primary history model

    - `core.tests.abstract.test_functional_history.HistoryEntriesChildModel` for child history model
