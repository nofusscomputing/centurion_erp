---
title: Entity
description: Centurion ERP Model Entity development documentation
date: 2025-04-03
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

An entity is either an organization or a person. This includes the grouping of such items. As this model is a core model, there is no need to create a new model. All that is required is that you inherit from the base entity model. From a higher level perspective, the model is intended to be used to build the entire chain of the intended entity you desire. For each additional "child-model", it must only contain the differences from the parent model. For example, to create a contact "entity", you would first create the Person model which will inherit for the Entity Model, then you create the contact model which will inherit from the Person model.


## History

[Audit History](./model_history.md) is included as part of the base model with there being no additional work required for audit history to work out of the box.


## Notes

[Model Notes](./model_notes.md) is included as part of the base model with there being no additional work required for notes to work out of the box.


## Model

When creating your model, do not re-define any field that is already specified within the model you are inheriting from. This is however, with the exception of the code docs specifying otherwise.


### Example model

This example demonstrates how the contact model is created. As a Contact is a person, there must also be a Person "Entity" created.

Create the person "Entity" only containing the fields for a "person"

``` py title="app/access/models/person.py"

--8<-- "app/access/models/person.py"

```

Now Create the contact "Entity" only containing the fields for a "contact"

``` py title="app/access/models/contact.py"

--8<-- "app/access/models/contact.py"

```

!!! tip
    Take note of the inheritance and the fact that children don't override parent objects.


## Testing

As with any other object within Centurion, the addition of a feature requires it be tested. The following Test Suites are available:

- `Unit` Test Cases

    - `access.tests.unit.contact.<*>.<Inherited class name>InheritedCases` _(if inheriting from `Contact`)_ Test cases for sub-models

    - `access.tests.unit.entity.<*>.<Inherited class name>InheritedCases` _(if inheriting from `Entity`)_ Test cases for sub-models

    - `access.tests.unit.people.<*>.<Inherited class name>InheritedCases` _(if inheriting from `Person`)_ Test cases for sub-models

- `Functional` Test Cases

    - `access.tests.functional.contact.<*>.<Inherited class name>InheritedCases` _(if inheriting from `Contact`)_ Test cases for sub-models

    - `access.tests.functional.entity.<*>.<Inherited class name>InheritedCases` _(if inheriting from `Entity`)_ Test cases for sub-models

    - `access.tests.functional.people.<*>.<Inherited class name>InheritedCases` _(if inheriting from `People`)_ Test cases for sub-models

The above listed test cases cover **all** tests for objects that are inherited from the base class. To complete the tests, you will need to add test cases for the differences your model introduces.
