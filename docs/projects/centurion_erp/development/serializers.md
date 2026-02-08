---
title: Serializers
description: Centurion ERP Serializers development documentation
date: 2025-05-27
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Serializers within Centurion ERP are responsible for arranging the data for presentation to the user as well as sanitization and validation for incoming user data. As Centurion ERP is an API based application the serializer is crucial to its operation


## Introduction

Our Serializers are broken down into three different types, they are:

- Base Serializer

- Model Serializer

- View Serializer


### Base Serializer

The base serializer is a read-only serializer that returns only minimal data about a model, that being: id, display name and url. Even though this serializer only returns minimal data, it's crucial data that the interfact uses for linking data between models.


### Model Serializer

The Model serializer is the write capable serializer and is used for both add and update actions. This serializer is also responsible for the sanitization and validation of user provided data.

!!! tip
    Models can also be responsible for validating data as well. Ensure that you dont add to your serializer validation logic that the [model is responsible](./models.md#validation-methods) for.


### View Serializer

The View serializer as the name implies is for viewing a model. Unlike the model serializer, this serializer will return all linked fields (model related fields) using that models base serializer. This serializer is also used to return an object as part of a CRUD operation.


## Creating a Serializer

All serializers are placed within a module under a directory called `serializers`. For clarification serializers are named according to its models name (`<model>._meta.model_name`). for sub-models this name is prefixed with `<base model>._meta.model_name_`.

!!! danger
    Failing to use this naming schema will caused a crash as the serializers cant be located by the _"loader"_


### Requirements

When creating a serializer, the following requirements must be met:

- inherits from:

    - Thier preceeding serializer. i.e. `View` inherits `Model` which inherits `Base`

    - View serializer, `api.serializers.common.CommonModelSerializer`

- Follows file naming as described [above](#creating-a-serializer)

- `Base` serializer must return fields `id`, `display_name` and `url`, with url being the models url

- `View` serializer must return a dict field called `_urls` which contains links to the models [core features](./models.md#core-features), including `_self`

- **All** Serializer exceptions must be from `rest_framework.exceptions`


## Available Serializers

With the exception of Centurion ERP models, the following additional serializers are available:

- User `centurion.serializers.content_type`

- User `centurion.serializers.permission`

- User `centurion.serializers.user`
