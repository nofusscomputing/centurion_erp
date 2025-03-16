---
title: Feature Flags
description: Feature Flag component Documentation for Centurion ERP by No Fuss Computing
date: 2025-03-02
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Feature flags are a tool that a developer can use so as to conduct progressive releases. That is by hiding a feature behind a flag that is only enabled (available to end users) when it is marked as enabled. Feature Flagging is slightly different to other models within Centurion in that you can't across organizations use it's feature. Feature Flagging is enabled on a per organization basis.


## Fields

- **ID** Primary Key / ID of the feature flag. _This field is hidden and automagically generated. ID is viewable from the API endpoint_

- **Name** Arbitrary name for this feature flag

- **Description** Arbitrary description for this feature flag

- **Enabled** Is this feature enabled

- **Software** The software this feature flag belongs

- **created** Date and time the feature flag was created

- **modified** Date and time the feature flag was modified


## Enabling Feature Flagging

Until you enable feature flagging within the organization you intend on using it. You will not be able to add feature flagging for the software in question.

To enable feature flagging navigate to the software in question `ITAM -> Software`, enter the software page and click on the `Feature Flagging` tab. Click the `Add` button, then select the organization, software and enabled. Once you save this form, youi will be able to add the feature flag.


## API Endpoint

!!! danger
    The Feature Flag Endpoint (`api/v2/public/<organization_id>/flags/<software_id>`) is publicly accessible. i.e. does not require that a user log in to Centurion. This is by design. You are advised not to enter any sensitive information within the name or description fields of the feature flag.

The API endpoint that is available for feature flagging returns a paginated JSON document containing ALL of the feature flags for the software in question. The format of this document is as follows.

``` jsonc
{
    "results": [

        {
            "2025-00001": {                              // ID of the feature (format: YYYY-<Feature ID>, using year of creation), Dictionary
                "name": "Feature name 1",                // String
                "description": "Feature description",    // String
                "enabled": true,                         // Boolean
                "created": "Date time created",          // String
                "modified": "Date time modified"         // String
            }
        },
        {
            "2025-00002": {
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
            "count": 2
        }
    },
    "links": {
        "first": "https://mydomain.tld/api/v2/public/1/flags/1234?page%5Bnumber%5D=1",
        "last": "https://mydomain.tld/api/v2/public/1/flags/1234?page%5Bnumber%5D=1",
        "next": null,
        "prev": null
    }
}
```

The url for the feature flags can be found at API endpoint `api/v2/public/flags`. This view displays a dictionary of organizations by name with each organization showing the available urls by software name.


### Using the endpoint in your software

The software you are developing will need to be able to query the flags endpoint, including the ability to obtain paginated results. As JSON is returned from the endpoint there is no restriction upon what programming language you are using. The only requirement is the ability to parse JSON. Most if not all programming languages can do this.

A simple query to the endpoint is all that is required. As only 10 results are returned per page, if `meta.pagination.pages > 1` subsequent requests will be required to obtain all available feature flags. Once you have the complete document, a simple `if` statement is all that is required. i.e. `if flags_json['2025-00001']['enabled']`.

The Feature Flags endpoint does support HTTP Header `If-Modified-Since`. The value of this field is passed when you make a request to the Feature Flag endpoint within header `Last-Modified`. The value of the `Last-Modified` header is derived from the most recently edited feature flag that was received from the endpoint. Simply put, if you failed to parse the `Last-Modified` header, you can iterate over the list of feature flags you received and use the most recent modified date.

!!! tip
    HTTP header Date fields must be correctly formatted. please see [RFC1910 - 5.6.7. Date/Time Formats](https://httpwg.org/specs/rfc9110.html#http.date) for more details.
