---
title: Ticket
description: Centurion ERP Base Model Ticket development documentation
date: 2025-04-16
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Ticketing is a base model within Centurion ERP. This base provides the core features for all subsequent sub-ticket models. As such extending Centurion ERP with a new ticket type is a simple process. The adding of a ticket type only requires that you extend an existing ticket model containing only the changes for your new ticket type.


## Core Features

- Centurion Object assosiate to ticket


## Assosiate object to ticket

All models within Centruion ERP can be assosiated to a ticket unless otherwise stated. Whenever the model is created, a meta model is created and used at runtime.


## History

Ticketing does not use the standard history model of Centurion ERP. History for a ticket is kept in the form of action comments. As each change to a ticket occurs, an action comment is created denoting the from and to in relation to a change.


## Model

When creating your sub-model, do not re-define any field that is already specified within the model you are inheriting from. This is however, with the exception of the code docs specifying otherwise.


## Testing

As with any other object within Centurion, the addition of a feature requires it be tested. Test for ticketing follows the [model](../models.md#tests) test suites, however the source for the inherited tests are the ticket tests that your model inherits from. for instance if you extend `TicketBase`, your test suits will inherit from `TicketBase` model tests.
