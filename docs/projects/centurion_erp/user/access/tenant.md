---
title: Tenant
description: Tenant Documentation for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

An tenant is how multi-tenancy is conducted within this application. All data within the application is tied to an tenant and only users whom are members of the tenancy with the correct permission can view that item within an tenancy.


## Tenant Manager

A tenant manager is to be viewed as the "owner" of an tenant. With the exception of editing the tenant itself, the manager can conduct **ALL** operations against an tenant regardless of their permissions.
