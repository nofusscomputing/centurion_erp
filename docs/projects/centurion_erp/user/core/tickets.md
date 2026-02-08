---
title: Tickets
description: Ticket system Documentation as part of the Core Module for Centurion ERP by No Fuss Computing
date: 2024-08-23
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

A ticket within Centurion ERP is an item of work. Its intent is to capture all of the required data for the lifecycle of the work item.


## Features

- Commenting

- Linked Items to ticket

- [Markdown](./markdown.md) support within the ticket description and comment(s)

- Parent / Child Tickets

- Project

- Slash commands

- Ticket Dependencies


## Fields

As tickets are a core feature, most ticket will contain the fields below. With exception to the fields marked "Mandatory" Most fields are only available for a ticket triage user.

- [`Organization`](../access/tenant.md) Tenancy where the ticket should be created. ***Mandatory***

- `Title` Title of the ticket. ***Mandatory***

- `Description` Description for the ticket. ***Mandatory***

- `External System` External sysem ID. ***Optional***

    !!! note
        This field is only available for a user with import permissions

- `Reference Number` External system ticket number. ***Optional***

    !!! note
        This field is only available for a user with import permissions

- `Parent Ticket` Parent ticket of this ticket. ***Optional***

- [`Status`](#ticket-status) Status of this ticket. ***Optional***

- [`Category`](./ticketcategory.md) Category of this ticket. _User requires triage permission._ ***Optional***

- `Private` Mark ticket as private. ***Optional***

- [`Project`](../project_management/project.md) Project this ticket belongs to. _User requires triage permission._ ***Optional***

- `Project Milestone` Milestone for this ticket. _User requires triage permission._ ***Optional***

- `Urgency` Urgency for this ticket to be solved from the ticket raiser. ***Optional***

- `Impact` Assessed impact of this ticket. _User requires triage permission._ ***Optional***

- `Priority` Work completion order of this ticket. _User requires triage permission._ ***Optional***

- `Opened By` Whom opened the ticket. ***Optional***

- `Subscribers` User / Groups whom are subscribed to obtain updates of this ticket. ***Optional***

- `Assignees` User / Groups whom are assigned to work on this ticket. _User requires triage permission._ ***Optional***

- `Planned Start Date` When the ticket is planned to be started by. _User requires triage permission._ ***Optional***

- `Planned Finish Date` When the ticket is planned to be completed by. _User requires triage permission._ ***Optional***

- `Real Start Date` When the ticket work actually started. _User requires triage permission._ ***Optional***

- `Real Finish Date` When the ticket work actually finished. _User requires triage permission._ ***Optional***

In Addition, tickets also contain the following objects for each ticket:

- `Dependencies` Other related tickets, (related, blocked and blocked by). ***Optional***

- [`Linked Models`](#linking-items-to-a-ticket) Models the ticket is related to. ***Optional***


## Creating a Ticket

Complete all of the required fields and click save. The following rules apply when creating a ticket:

- Ticket must have a non-blank title.

- If a project is selected, the milestone must come from the same project.


## Linking items to a ticket

Nearly all items within Centurion ERP can be linked to a ticket. To find out if an item can be linked to a ticket nevigate to its details page and if you see a tickets tab, the model can be linked to a ticket.

To link an object to a ticket use slash command `/link` with the objects [model tag](./markdown.md#model-reference--model-tag).


## Ticket Status'

Tickets have status' which are a simple way of denoting the stage a ticket is at. The common status' available are:

- Draft

    A ticket with a draft status denotes the ticket has not been submitted and that the ticket raiser is still working on the ticket.

- New

    A ticket with a new status denotes the ticket is submitted and ready for triage.

- Assigned

    A ticket with an assigned status is being worked on. The assigned field will also have the person/team who is assigned to work on the ticket.

- Assigned (planning)

    A ticket with an assigned-planning status is a ticket that has been scheduled to work on. like the assigned status, the tickets assigned field will contain the person / team whom is working on the ticket.

- Pending

    A ticket with a pending status means that the ticket is on hold for some reason.

- Solved

    A ticket with the solved status means that all work has been completed on the ticket.

- Invalid

    A ticket with a status of invalid, means that the ticket was raised in error.

- Closed

    A ticket with a closed status means that no more changes can be made to the ticket as it has been solved with all work complete.

Some of the status' above auto-magic change when a field changes on a ticket or some other action related to a ticket. for example:

- Assigning a ticket to a person/team will set the ticket status to `Assigned`

- Posting a solution comment will set the ticket status to solved. This is on the proviso that the ticket is solvable.


## Solving a ticket

Solving a ticket is not as simple as setting the status of the ticket to `Solved`. There is validation to ensure that you cant solve a ticket that is considered incomplete. An incomplete ticket is so if it meets any of the following criteria:

- Any comment is not in a closed state

When all of the incomplete criteria is complete, you can set the ticket to `Solved` or post a solution comment.


## Commenting

Ticket comments support [markdown](./markdown.md) as well as slash commands. Comments are broken down into different types, they are:

- Standard

    A typical comment that has the ability to track time spent, have a category assigned as well as a source for the comment.

- ~~Notification _Change, Incident, Problem, Project Tasks and Request tickets.~~_ _awaiting [github-564](https://github.com/nofusscomputing/centurion_erp/issues/564)_

- Solution

    A solution comment has all of the features a standard comment has. In addition, leaving this type of comment will mark the ticket as solved as long as it meets the [criteria](#solving-a-ticket).

    !!! info
        To add this type of comment, you will require the `triage` permission for the ticket type the comment is for.

- Task

    A task comment as the name implies is for recording and categorising work done on a ticket. This type of ticket is reserverd for a user whom has the `triage` permission for the ticket being worked on.

    !!! info
        To add this type of comment, you will require the `triage` permission for the ticket type the comment is for.


## Slash Commands

Slash commands are a quick action that is specified after a slash command. As the name implies, the command starts with a slash `/`. The following slash commands are available:

- Linked Item `/link` i.e. to link device 22 (`id`/`number` in device details page url ) the command would be `/link $device-22`. to see the available model references / model tag, please see the [markdown docs](./markdown.md#model-reference--model-tag).

    Enables you to link different objects from Centurion ERP to a ticket. Once an object has been linked to ticket you will see the ticket within the objects details page under the ticket tab.

- Related `/blocked_by`, `/blocks` and `/relate` i.e. to mark ticket 22 as related, use `/relate #22`

- Time Spent `/spend`, `/spent` i.e. to record 3 hours and 5 mins of time spent, use `/spend 3h5m`

When using slash commands, there is only to be one slash command per line. All slash commands support reference stacking (more than one reference) as long as they are separated by a space. i.e. `/<command> $<model>-<pk> $<model>-<pk> $<model>-<pk>`


### Time Spent

::: app.core.lib.slash_commands.CommandTimeTrack
    options:
        inherited_members: false
        members: []
        show_bases: false
        show_submodules: false
        summary: true


### Linked Items

::: app.core.lib.slash_commands.CommandLinkModelTicket
    options:
        inherited_members: false
        members: []
        show_bases: false
        show_submodules: false
        summary: true


### Ticket Dependencies

::: app.core.lib.slash_commands.CommandTicketDependency
    options:
        inherited_members: false
        members: []
        show_bases: false
        show_submodules: false
        summary: true


## Re-Opening a Ticket

To re-open a ticket is as simple as changing the status and saving. Not everyone can re-open a ticket, it depends upon the following:

- The user who raised the ticket can re-open the ticket only when the status is `SOLVED`

- A User with `Triage` permission can re-open a ticket when the status is `SOLVED` or `CLOSED` regardless of who raised the ticket.
