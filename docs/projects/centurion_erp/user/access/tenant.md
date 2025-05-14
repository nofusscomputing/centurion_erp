---
title: Tenant
description: Tenant Documentation for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

An tenant is how multi-tenancy is conducted within this application. All data within the application is tied to an tenant and only users whom are members of the tenant with the correct permission can view that item within an tenant.

!!! warning
    Any object within any tenant that has been marked as `global`. Any user whom has the correct `view` permission will be able to see the global object. 
    
    _**Note:**: This does not include other items that may be attached to the global object that is itself not marked as global._


## Tenant Manager

A tenant manager is to be viewed as the "owner" of an tenant. With the exception of editing the tenant itself, the manager can conduct **ALL** operations against an tenant regardless of their permissions. An orgnization manager does not need any permissions to add, change delete or view a `Team` or `Team User`. This also includes not requiring the `view` permission for an `Tenant`.
