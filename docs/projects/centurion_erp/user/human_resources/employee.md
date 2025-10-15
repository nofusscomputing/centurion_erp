---
title: Employee
description: Employee as part of Human Resources User Documentation for Centurion ERP by No Fuss Computing
date: 2025-04-15
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

This component within HR is for the management of an organizations employee(s).


## Fields

This model shares all of the fields that are available for a [contact](../access/contact.md#fields). additionally employee also has field(s):

- `employee number` An internal number to reference the employee. ***Mandatory***

- `user` The Centurion ERP user account associated with this employee. ***Optional***


## Creating an Employee

Complete all of the required fields and click save. The following rules apply when creating an employee:

- `Employee Number` must be unique.

- As an employee is a sub-object of a `Contact` its [rules apply](../access/contact.md#creating-a-contact) too.