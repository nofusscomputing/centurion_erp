---
title: Feature Flags
description: Feature Flag administration Documentation for Centurion ERP by No Fuss Computing
date: 2025-03-02
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

[Feature flags](../../user/devops/feature_flags.md) is available out off the box. Although if you have followed the recommended practice of deploying Centurion ERP from behind a reverse proxy, you will need to setup the reverse proxy to pass through to the flags endpoint.


## Setup

For feature flagging to function, the endpoint needs to be made available publicly. This endpoint is exposed from the API container on url `/public/`, more specifically `/public/flags/<software id>`. `<software id>` is the primary key for the software the feature flags are for.

It's completely your choice how you expose this endpoint although with the caveat that no authentication is required. You can expose endpoint `/public/flags/<software id>` or `/public/flags`. The former will require for any additional software that has feature flagging enabled, that its endpoint also be exposed. Choosing the latter over the former will bare no consequence as attempting to access an endpoint for a piece of software that has not had feature flagging enabled or does not exist, will cause a `HTTP/404` to be returned. Other status codes that may be returned from this endpoint are:

- `HTTP/304 - Not Modified`

    When a client checks-in and if they supply request header `If-Modified-Since:` with its value set to the last modified feature flag they have. If no feature flag has been updated, this status will be returned with an empty response body.

- `HTTP/200 - Success`

    When the client checks-in and the feature flags have been supplied. If the user does not specify request header `If-Modified-Since:`, the feature flags will always be returned.


## Settings

Within your settings file the following settings are available

| Attribute | Type | Default | Description |
|:---|:---:|:---:|:---|
| FEATURE_FLAGGING_ENABLED | `Boolean` | `True `| Turn feature flagging on/off. |
| FEATURE_FLAG_OVERRIDES | `list(dict)` | `None` | Feature Flags to override. Uses same format as the API Enbdpoint. |
