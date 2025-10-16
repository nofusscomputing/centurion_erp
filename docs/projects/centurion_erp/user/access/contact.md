---
title: Contacts Directory
description: Centurion ERP Contacts Directory user documentation
date: 2025-04-04
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

The Contacts Directory / Corporate Directory simply put is the equivalent of a phone book. Within this directory you will be able to find the contact details of any contact you have access to view.


## Fields

A contact has field(s):

- `First Name` The contacts first name. ***Mandatory***

- `Middle Name` The contacts middle name(s). ***Optional***

- `Last Name` The contacts last name. ***Mandatory***

- `DOB` The contacts Date of Birth. ***Optional***

- `E-Mail` The contacts E-Mail address. ***Mandatory***

- `Show in directory` Show this contact in the directory. ***Mandatory**


## Creating a Contact

Complete all of the required fields and click save. The following rules apply when creating a contact:

- The contacts `E-Mail` address must be unique.

- As a contact is a sub-object of a `Person` the following additional rules apply:

    - fields (`First Name`, `Middle Name`, `Last Name` and `DOB`) or (`First Name`, `Last Name` and `DOB`) or (`First Name`, `Last Name`) must be unique. _checked in the listed order._

When creating a contact, if an existing person is found that matches the persons details, it will not be re-created. The existing person will be linked to the new contact.
