---
title: Model Notes
description: Centurion ERP Model Notes development documentation
date: 2025-02-09
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Model Notes is a core feature that is intended to be used so that users can place comments against a model. These comments are arbitrary. [Markdown](../../user/core/markdown.md) is supported. All Tenancy Models have model notes enabled by default.


## Adding Model Notes to a Model

By default there is nothing that you need to do to add Model Notes to a model. By virtue of inheriting from [`core.models.centurion.CenturionModel`](../api/models/centurion.md) or `core.models.centurion.CenturionSubModel` the model will have model notes setup automagically. This wizardry of the machine creates all of the necessary components that the moment you run the migrations the model has a fully functioning model notes system.
