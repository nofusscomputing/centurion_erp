---
title: Feature Flags
description: Feature Flag component Documentation for Centurion ERP by No Fuss Computing
date: 2025-03-02
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Feature flags are a tool that a developer can use so as to conduct progressive releases. That is by hiding a feature behind a flag that is only enabled (available to end users) when it is marked as enabled.


## Fields

- **ID** Primary Key / ID of the feature flag. _This field is hidden and automagically generated. ID is viewable from the API endpoint_

- **Name** Arbitrary name for this feature flag

- **Description** Arbitrary description for this feature flag

- **Enabled** Is this feature enabled

- **Software** The software this feature flag belongs

- **created** Date and time the feature flag was created

- **modified** Date and time the feature flag was modified


## API Endpoint

!!! danger
    The Feature Flag Endpoint is publicly accessible. i.e. does not require that a user log in to Centurion. This is by design. You are advised not to enter any sensitive information within the name or description fields of the feature flag.

The API endpoint that is available for feature flagging returns a paginated JSON document containing ALL of the feature flags for the software in question. The format of this document is as follows.

``` jsonc
{
    "results": [

        {
            "2025-0001": {                               // ID of the feature (format: YYYY-<Feature ID>, using year of creation), Dictionary
                "name": "Feature name 1",                // String
                "description": "Feature description",    // String
                "enabled": true,                         // Boolean
                "created": "Date time created",          // String
                "modified": "Date time modified"         // String
            }
        },
        {
            "2025-0002": {
                "name": "Feature name 2",
                "description": "Feature description",
                "enabled": true,
                "created": "Date time created",
                "modified": "Date time modified"
            }
        }
    ],
    "meta": {
        "pagination": {
            "page": 1,
            "pages": 1,
            "count": 1
        }
    },
    "links": {
        "first": "https://mydomain.tld/public/flags/1234?page%5Bnumber%5D=1",
        "last": "https://mydomain.tld/public/flags/1234?page%5Bnumber%5D=1",
        "next": null,
        "prev": null
    }
}
```


### Using the endpoint in your software

The software you are developing will need to be able to query the flags endpoint, including the ability to obtain paginated results. As JSON is returned from the endpoint there is no restriction upon what programming language you are using. The only requirement is the ability to parse JSON. Most if not all programming languages can do this.

A simple query to the endpoint is all that is required. As only 10 results are returned per page, if `meta.pagination.pages > 1` subsequent requests will be required to obtain all available feature flags. Once you have the complete document, a simple `if` statement is all that is required. i.e. `if flags_json['2025-0001']['enabled']`.
