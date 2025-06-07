---
title: Model Audit History
description: Centurion ERP Model Audit History development documentation
date: 2025-02-15
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Model Audit History is a core feature that is intended to be used to keep an audit history of **ALL** changes to a model. All Tenancy Models are to have a history model created for it.


## Adding History to a Model

By default there is nothing that you need to do to add Audit History to a model. By virtue of inheriting from [`core.models.centurion.CenturionModel`](../api/models/centurion.md) or [`core.models.centurion.CenturionSubModel`](../api/models/centurion_sub.md) the model will have audit history setup automagically. This wizardry of the machine creates all of the necessary components that the moment you run the migrations the model has a fully functioning audit history system.
