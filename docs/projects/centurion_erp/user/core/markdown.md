---
title: Markdown
description: Markdown Documentation as part of the Core Module for Centurion ERP by No Fuss Computing
date: 2024-09-11
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

All Text fields, that is those that are multi-lined support markdown text.


## Features

- CommonMark Markdown

- Tables

- Strikethrough

- Code highlighting

- Admonitions

- Linkify

- Task Lists

- Heading Anchors

- Ticket References

- Model References


## Admonitions


![admonition example](../images/admonition-example.png)

declare with:

``` md

!!! <type> "<optional heading in double quotes>"
    text goes here

```

Available admonition types are:

- note

- info

- tip

- warning

- danger

- quote


## Ticket References

Declare a ticket reference in format `#<ticket number>`, and it will be rendered as a link to the ticket. i.e. `#2`


## Model Reference / Model Tag

A Model link is a reference to an item within the database. Supported model link items are:

| Model | Tag |
|:---|:---:|
| cluster| `$cluster-<id>` |
| clustertype| `$-<id>` |
| config groups| `$config_group-<id>` |
| device| `$device-<id>` |
| devicemodel| `$-<id>` |
| devicetype| `$-<id>` |
| externallink| `$-<id>` |
| group| `$-<id>` |
| knowledgebase| `$kb-<id>` |
| knowledgebasecategory| `$-<id>` |
| manufacturer| `$-<id>` |
| modelnotes| `$-<id>` |
| operatingsystem| `$operating_system-<id>` |
| operatingsystemversion| `$-<id>` |
| organization| `$organization-<id>` |
| port| `$-<id>` |
| project| `$-<id>` |
| projectmilestone| `$-<id>` |
| projectstate| `$-<id>` |
| projecttask| `$-<id>` |
| projecttype| `$-<id>` |
| service| `$service-<id>` |
| software| `$software-<id>` |
| softwarecategory| `$-<id>` |
| softwareversion| `$-<id>` |
| team| `$team-<id>` |
| ticketcategory| `$-<id>` |
| ticketcomment| `$-<id>` |
| ticketcommentcategory| `$-<id>` |

To declare a model link use syntax `$<type>-<model id>`. i.e. for device 1, it would be `$device-1`
