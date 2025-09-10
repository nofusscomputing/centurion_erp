---
title: Centurion ERP
description: Documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

<span style="text-align: center;">

![Project Status - Active](https://img.shields.io/badge/Project%20Status-Active-green?logo=github&style=plastic)

![Docker Pulls](https://img.shields.io/docker/pulls/nofusscomputing/centurion-erp?style=plastic&logo=docker&color=0db7ed) [![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/centurion-erp)](https://artifacthub.io/packages/container/centurion-erp/centurion-erp)

![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Frefs%2Fheads%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fmaster%2Fbadge_endpoint_integration_postgres_versions.json&style=plastic&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iNDMyLjA3MXB0IiBoZWlnaHQ9IjQ0NS4zODNwdCIgdmlld0JveD0iMCAwIDQzMi4wNzEgNDQ1LjM4MyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgaWQ9Im9yZ2luYWwiIHN0eWxlPSJmaWxsLXJ1bGU6bm9uemVybztjbGlwLXJ1bGU6bm9uemVybztzdHJva2U6IzAwMDAwMDtzdHJva2UtbWl0ZXJsaW1pdDo0OyI%2BCgk8L2c%2BCjxnIGlkPSJMYXllcl94MDAyMF8zIiBzdHlsZT0iZmlsbC1ydWxlOm5vbnplcm87Y2xpcC1ydWxlOm5vbnplcm87ZmlsbDpub25lO3N0cm9rZTojRkZGRkZGO3N0cm9rZS13aWR0aDoxMi40NjUxO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2UtbWl0ZXJsaW1pdDo0OyI%2BCjxwYXRoIHN0eWxlPSJmaWxsOiMwMDAwMDA7c3Ryb2tlOiMwMDAwMDA7c3Ryb2tlLXdpZHRoOjM3LjM5NTM7c3Ryb2tlLWxpbmVjYXA6YnV0dDtzdHJva2UtbGluZWpvaW46bWl0ZXI7IiBkPSJNMzIzLjIwNSwzMjQuMjI3YzIuODMzLTIzLjYwMSwxLjk4NC0yNy4wNjIsMTkuNTYzLTIzLjIzOWw0LjQ2MywwLjM5MmMxMy41MTcsMC42MTUsMzEuMTk5LTIuMTc0LDQxLjU4Ny03YzIyLjM2Mi0xMC4zNzYsMzUuNjIyLTI3LjcsMTMuNTcyLTIzLjE0OGMtNTAuMjk3LDEwLjM3Ni01My43NTUtNi42NTUtNTMuNzU1LTYuNjU1YzUzLjExMS03OC44MDMsNzUuMzEzLTE3OC44MzYsNTYuMTQ5LTIwMy4zMjIgICAgQzM1Mi41MTQtNS41MzQsMjYyLjAzNiwyNi4wNDksMjYwLjUyMiwyNi44NjlsLTAuNDgyLDAuMDg5Yy05LjkzOC0yLjA2Mi0yMS4wNi0zLjI5NC0zMy41NTQtMy40OTZjLTIyLjc2MS0wLjM3NC00MC4wMzIsNS45NjctNTMuMTMzLDE1LjkwNGMwLDAtMTYxLjQwOC02Ni40OTgtMTUzLjg5OSw4My42MjhjMS41OTcsMzEuOTM2LDQ1Ljc3NywyNDEuNjU1LDk4LjQ3LDE3OC4zMSAgICBjMTkuMjU5LTIzLjE2MywzNy44NzEtNDIuNzQ4LDM3Ljg3MS00Mi43NDhjOS4yNDIsNi4xNCwyMC4zMDcsOS4yNzIsMzEuOTEyLDguMTQ3bDAuODk3LTAuNzY1Yy0wLjI4MSwyLjg3Ni0wLjE1Nyw1LjY4OSwwLjM1OSw5LjAxOWMtMTMuNTcyLDE1LjE2Ny05LjU4NCwxNy44My0zNi43MjMsMjMuNDE2Yy0yNy40NTcsNS42NTktMTEuMzI2LDE1LjczNC0wLjc5NywxOC4zNjdjMTIuNzY4LDMuMTkzLDQyLjMwNSw3LjcxNiw2Mi4yNjgtMjAuMjI0ICAgIGwtMC43OTUsMy4xODhjNS4zMjUsNC4yNiw0Ljk2NSwzMC42MTksNS43Miw0OS40NTJjMC43NTYsMTguODM0LDIuMDE3LDM2LjQwOSw1Ljg1Niw0Ni43NzFjMy44MzksMTAuMzYsOC4zNjksMzcuMDUsNDQuMDM2LDI5LjQwNmMyOS44MDktNi4zODgsNTIuNi0xNS41ODIsNTQuNjc3LTEwMS4xMDciLz4KPHBhdGggc3R5bGU9ImZpbGw6IzMzNjc5MTtzdHJva2U6bm9uZTsiIGQ9Ik00MDIuMzk1LDI3MS4yM2MtNTAuMzAyLDEwLjM3Ni01My43Ni02LjY1NS01My43Ni02LjY1NWM1My4xMTEtNzguODA4LDc1LjMxMy0xNzguODQzLDU2LjE1My0yMDMuMzI2Yy01Mi4yNy02Ni43ODUtMTQyLjc1Mi0zNS4yLTE0NC4yNjItMzQuMzhsLTAuNDg2LDAuMDg3Yy05LjkzOC0yLjA2My0yMS4wNi0zLjI5Mi0zMy41Ni0zLjQ5NmMtMjIuNzYxLTAuMzczLTQwLjAyNiw1Ljk2Ny01My4xMjcsMTUuOTAyICAgIGMwLDAtMTYxLjQxMS02Ni40OTUtMTUzLjkwNCw4My42M2MxLjU5NywzMS45MzgsNDUuNzc2LDI0MS42NTcsOTguNDcxLDE3OC4zMTJjMTkuMjYtMjMuMTYzLDM3Ljg2OS00Mi43NDgsMzcuODY5LTQyLjc0OGM5LjI0Myw2LjE0LDIwLjMwOCw5LjI3MiwzMS45MDgsOC4xNDdsMC45MDEtMC43NjVjLTAuMjgsMi44NzYtMC4xNTIsNS42ODksMC4zNjEsOS4wMTljLTEzLjU3NSwxNS4xNjctOS41ODYsMTcuODMtMzYuNzIzLDIzLjQxNiAgICBjLTI3LjQ1OSw1LjY1OS0xMS4zMjgsMTUuNzM0LTAuNzk2LDE4LjM2N2MxMi43NjgsMy4xOTMsNDIuMzA3LDcuNzE2LDYyLjI2Ni0yMC4yMjRsLTAuNzk2LDMuMTg4YzUuMzE5LDQuMjYsOS4wNTQsMjcuNzExLDguNDI4LDQ4Ljk2OWMtMC42MjYsMjEuMjU5LTEuMDQ0LDM1Ljg1NCwzLjE0Nyw0Ny4yNTRjNC4xOTEsMTEuNCw4LjM2OCwzNy4wNSw0NC4wNDIsMjkuNDA2YzI5LjgwOS02LjM4OCw0NS4yNTYtMjIuOTQyLDQ3LjQwNS01MC41NTUgICAgYzEuNTI1LTE5LjYzMSw0Ljk3Ni0xNi43MjksNS4xOTQtMzQuMjhsMi43NjgtOC4zMDljMy4xOTItMjYuNjExLDAuNTA3LTM1LjE5NiwxOC44NzItMzEuMjAzbDQuNDYzLDAuMzkyYzEzLjUxNywwLjYxNSwzMS4yMDgtMi4xNzQsNDEuNTkxLTdjMjIuMzU4LTEwLjM3NiwzNS42MTgtMjcuNywxMy41NzMtMjMuMTQ4eiIvPgo8cGF0aCBkPSJNMjE1Ljg2NiwyODYuNDg0Yy0xLjM4NSw0OS41MTYsMC4zNDgsOTkuMzc3LDUuMTkzLDExMS40OTVjNC44NDgsMTIuMTE4LDE1LjIyMywzNS42ODgsNTAuOSwyOC4wNDVjMjkuODA2LTYuMzksNDAuNjUxLTE4Ljc1Niw0NS4zNTctNDYuMDUxYzMuNDY2LTIwLjA4MiwxMC4xNDgtNzUuODU0LDExLjAwNS04Ny4yODEiLz4KPHBhdGggZD0iTTE3My4xMDQsMzguMjU2YzAsMC0xNjEuNTIxLTY2LjAxNi0xNTQuMDEyLDg0LjEwOWMxLjU5NywzMS45MzgsNDUuNzc5LDI0MS42NjQsOTguNDczLDE3OC4zMTZjMTkuMjU2LTIzLjE2NiwzNi42NzEtNDEuMzM1LDM2LjY3MS00MS4zMzUiLz4KPHBhdGggZD0iTTI2MC4zNDksMjYuMjA3Yy01LjU5MSwxLjc1Myw4OS44NDgtMzQuODg5LDE0NC4wODcsMzQuNDE3YzE5LjE1OSwyNC40ODQtMy4wNDMsMTI0LjUxOS01Ni4xNTMsMjAzLjMyOSIvPgo8cGF0aCBzdHlsZT0ic3Ryb2tlLWxpbmVqb2luOmJldmVsOyIgZD0iTTM0OC4yODIsMjYzLjk1M2MwLDAsMy40NjEsMTcuMDM2LDUzLjc2NCw2LjY1M2MyMi4wNC00LjU1Miw4Ljc3NiwxMi43NzQtMTMuNTc3LDIzLjE1NWMtMTguMzQ1LDguNTE0LTU5LjQ3NCwxMC42OTYtNjAuMTQ2LTEuMDY5Yy0xLjcyOS0zMC4zNTUsMjEuNjQ3LTIxLjEzMywxOS45Ni0yOC43MzljLTEuNTI1LTYuODUtMTEuOTc5LTEzLjU3My0xOC44OTQtMzAuMzM4ICAgIGMtNi4wMzctMTQuNjMzLTgyLjc5Ni0xMjYuODQ5LDIxLjI4Ny0xMTAuMTgzYzMuODEzLTAuNzg5LTI3LjE0Ni05OS4wMDItMTI0LjU1My0xMDAuNTk5Yy05Ny4zODUtMS41OTctOTQuMTksMTE5Ljc2Mi05NC4xOSwxMTkuNzYyIi8%2BCjxwYXRoIGQ9Ik0xODguNjA0LDI3NC4zMzRjLTEzLjU3NywxNS4xNjYtOS41ODQsMTcuODI5LTM2LjcyMywyMy40MTdjLTI3LjQ1OSw1LjY2LTExLjMyNiwxNS43MzMtMC43OTcsMTguMzY1YzEyLjc2OCwzLjE5NSw0Mi4zMDcsNy43MTgsNjIuMjY2LTIwLjIyOWM2LjA3OC04LjUwOS0wLjAzNi0yMi4wODYtOC4zODUtMjUuNTQ3Yy00LjAzNC0xLjY3MS05LjQyOC0zLjc2NS0xNi4zNjEsMy45OTR6Ii8%2BCjxwYXRoIGQ9Ik0xODcuNzE1LDI3NC4wNjljLTEuMzY4LTguOTE3LDIuOTMtMTkuNTI4LDcuNTM2LTMxLjk0MmM2LjkyMi0xOC42MjYsMjIuODkzLTM3LjI1NSwxMC4xMTctOTYuMzM5Yy05LjUyMy00NC4wMjktNzMuMzk2LTkuMTYzLTczLjQzNi0zLjE5M2MtMC4wMzksNS45NjgsMi44ODksMzAuMjYtMS4wNjcsNTguNTQ4Yy01LjE2MiwzNi45MTMsMjMuNDg4LDY4LjEzMiw1Ni40NzksNjQuOTM4Ii8%2BCjxwYXRoIHN0eWxlPSJmaWxsOiNGRkZGRkY7c3Ryb2tlLXdpZHRoOjQuMTU1O3N0cm9rZS1saW5lY2FwOmJ1dHQ7c3Ryb2tlLWxpbmVqb2luOm1pdGVyOyIgZD0iTTE3Mi41MTcsMTQxLjdjLTAuMjg4LDIuMDM5LDMuNzMzLDcuNDgsOC45NzYsOC4yMDdjNS4yMzQsMC43Myw5LjcxNC0zLjUyMiw5Ljk5OC01LjU1OWMwLjI4NC0yLjAzOS0zLjczMi00LjI4NS04Ljk3Ny01LjAxNWMtNS4yMzctMC43MzEtOS43MTksMC4zMzMtOS45OTYsMi4zNjd6Ii8%2BCjxwYXRoIHN0eWxlPSJmaWxsOiNGRkZGRkY7c3Ryb2tlLXdpZHRoOjIuMDc3NTtzdHJva2UtbGluZWNhcDpidXR0O3N0cm9rZS1saW5lam9pbjptaXRlcjsiIGQ9Ik0zMzEuOTQxLDEzNy41NDNjMC4yODQsMi4wMzktMy43MzIsNy40OC04Ljk3Niw4LjIwN2MtNS4yMzgsMC43My05LjcxOC0zLjUyMi0xMC4wMDUtNS41NTljLTAuMjc3LTIuMDM5LDMuNzQtNC4yODUsOC45NzktNS4wMTVjNS4yMzktMC43Myw5LjcxOCwwLjMzMywxMC4wMDIsMi4zNjh6Ii8%2BCjxwYXRoIGQ9Ik0zNTAuNjc2LDEyMy40MzJjMC44NjMsMTUuOTk0LTMuNDQ1LDI2Ljg4OC0zLjk4OCw0My45MTRjLTAuODA0LDI0Ljc0OCwxMS43OTksNTMuMDc0LTcuMTkxLDgxLjQzNSIvPgo8cGF0aCBzdHlsZT0ic3Ryb2tlLXdpZHRoOjM7IiBkPSJNMCw2MC4yMzIiLz4KPC9nPgo8L3N2Zz4K)
 ![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Frefs%2Fheads%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fmaster%2Fbadge_endpoint_integration_rabbitmq_versions.json&style=plastic)

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nofusscomputing/centurion_erp/ci.yaml?branch=master&style=plastic&logo=github&label=Stable%20Build&color=%23000) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nofusscomputing/centurion_erp/ci.yaml?branch=development&style=plastic&logo=github&label=Dev%20Build&color=%23000)

![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/nofusscomputing/centurion_erp?style=plastic&logo=github&label=Open%20Issues&color=000) ![GitHub issue bugs](https://img.shields.io/github/issues-search?query=repo%3Anofusscomputing%2Fcenturion_erp%20type%3A%22Bug%22%20is%3Aopen%20&style=plastic&logo=github&label=Bug%20fixes%20required&color=000)

![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fdevelopment%2Fbadge_endpoint_coverage.json&style=plastic) ![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fdevelopment%2Fbadge_endpoint_unit_test.json)

![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fmaster%2Fbadge_endpoint_coverage_functional.json&style=plastic)
 ![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fmaster%2Fbadge_endpoint_functional_test.json)


</span>

Whilst there are many Enterprise Rescource Planning (ERP) applications, Centurion ERP is being developed to provide an open source option with a large emphasis on the IT Service Management (ITSM) modules. The goal is to provide a system that is not only an IT Information Library (ITIL), but that of which will connect to other ITSM systems, i.e. AWX for automation orchestration. Other common modules that form part of or are normally found within an ERP system, will be added if they relate specifically to any ITSM workflow. We welcome contributions should you desire a feature that does not yet exist.


## Documentation

Documentation is broken down into three areas, they are:

- [Administration](./administration/index.md)

- [Development](./development/index.md)

- [User](./user/index.md)

Specific features for a module can be found on the module's documentation un the features heading


## Development

It's important to us that Centurion ERP remaining stable. To assist with this we do test Centurion during it's development cycle. Testing reports are available and can be viewed from [Github](https://github.com/nofusscomputing/centurion_erp/actions/workflows/ci.yaml).

!!! info
    If you find any test that is less than sufficient, or does not exist; please let us know. If you know a better way of doing the test, even better. We welcome your contribution/feedback.


## Features

Feature table uses the following keys:

- :white_check_mark: Feature available.
- :recycle: Under development. Some features may be available.
- :x: Planned feature, development has not started.

| Module | Feature | Status | Notes |
|:---|:---|:---:|:---|
| **[Accounting](./user/accounting/index.md)** ||| _[see #88](https://github.com/nofusscomputing/centurion_erp/issues/88)_ |
|  | Asset Management | :recycle: | _[see #89](https://github.com/nofusscomputing/centurion_erp/issues/88)_ |
|  | General Ledger | :x: | [see #116](https://github.com/nofusscomputing/centurion_erp/issues/116) |
|  | Order Management | :x: | _[see #94](https://github.com/nofusscomputing/centurion_erp/issues/94)_ |
|  | Supplier Management | :x: | _[see #123](https://github.com/nofusscomputing/centurion_erp/issues/123)_ |
| **Core** |  |  |  |
|  | [API](./user/api.md) | :white_check_mark: |  |
|  | [Application wide settings](./user/settings/app_settings.md) | :white_check_mark: |  |
|  | [Audit History](./user/core/audit_history.md) | :white_check_mark: |  |
|  | [Corporate Directory (contacts)](./user/access/contact.md) | :white_check_mark: | _[see #705](https://github.com/nofusscomputing/centurion_erp/issues/705)_ |
|  | Location Management (Regions, Sites and Locations) | :x: | _[see #62](https://github.com/nofusscomputing/centurion_erp/issues/62)_ |
|  | [Markdown](./user/core/markdown.md) | :white_check_mark: |  |
|  | [Multi-Tenant](./user/access/tenant.md) | :white_check_mark: |  |
|  | [Roles (RBAC)](./user/access/role.md) | :white_check_mark: |  |
|  | [Single Sign-On {SSO}](./user/configuration.md#single-sign-on) | :white_check_mark: |  |
| **Customer Relationship Management (CRM)** || :x: | _[see #91](https://github.com/nofusscomputing/centurion_erp/issues/91)_  |
|  | Customers | :x: |  |
| **[Development Operations (DevOps)](./user/devops/index.md)**  ||| _[see #68](https://github.com/nofusscomputing/centurion_erp/issues/58)_ |
|  | [Feature Flags](./user/devops/feature_flags.md) | :white_check_mark: |  |
|  | [Repository Management](./user/devops/git_repository.md) | :recycle: | _[see #115](https://github.com/nofusscomputing/centurion_erp/issues/115)_ |
| **[Human Resource Management](./user/human_resources/index.md)**  || :recycle: | [see #92](https://github.com/nofusscomputing/centurion_erp/issues/92) |
|  | [Employee Management](./user/human_resources/employee.md) | :x: |  |
| **DCIM / ITIL / ITIM / ITSM** ||  |  |
|  | Bare Metal Provisioning | :x: |  |
|  | Certificate Management | :x: |  |
|  | Change Management | :recycle: |  |
|  | [Cluster Management](./user/itim/cluster.md) | :recycle: |  |
|  | [Configuration Management](./user/config_management/index.md) | :white_check_mark: |  |
|  | Database Management | :x: | _[see #72](https://github.com/nofusscomputing/centurion_erp/issues/72)_ |
|  | Incident Management | :recycle: |  |
|  | [IT Asset Management (ITAM)](./user/itam/index.md) | :white_check_mark: |  |
|  | [Knowledge Base](./user/assistance/knowledge_base.md) | :white_check_mark: |  |
|  | Licence Management | :x: | _[see #4](https://github.com/nofusscomputing/centurion_erp/issues/4)_ |
|  | Problem Management | :recycle: |  |
|  | Release and Deployment Management | :x: | _[see #462](https://github.com/nofusscomputing/centurion_erp/issues/462)_ |
|  | Request Management | :recycle: |  |
|  | Role Management | :x: | _[see #70](https://github.com/nofusscomputing/centurion_erp/issues/70)_ |
|  | Service Catalog | :x: | _[see #384](https://github.com/nofusscomputing/centurion_erp/issues/384)_ |
|  | Service level management | :recycle: | _[see #396](https://github.com/nofusscomputing/centurion_erp/issues/396)_ |
|  | [Service Management](./user/itim/service.md) | :white_check_mark: |  |
|  | Software Package Management | :x: | _[see #96](https://github.com/nofusscomputing/centurion_erp/issues/96)_ |
|  | Virtual Machine Management | :x: | _[see #73](https://github.com/nofusscomputing/centurion_erp/issues/73)_ |
|  | Vulnerability Management | :x: | _[see #3](https://github.com/nofusscomputing/centurion_erp/issues/3)_ |
| **[Project Management](./user/project_management/index.md)** || :white_check_mark: |  |
|  | [Milestones](./user/project_management/project.md#milestones) | :white_check_mark: |  |
|  | Roadmap | :x: |  |
| **Third party Integrations** ||  |  |
| | ArgoCD | :x: | [ArgoCD](https://github.com/argoproj-labs) is a Continuous Deployment system for ensuring objects deployed to kubernetes remain in the desired state. _[see #77](https://github.com/nofusscomputing/centurion_erp/issues/77)_ |
| | AWX | :x: | [AWX](https://github.com/ansible/awx) is an Automation Orchestration system that uses Ansible for its configuration. _[see #113](https://github.com/nofusscomputing/centurion_erp/issues/113)_ |
|  | [Companion Ansible Collection](../ansible/collection/centurion/index.md) | :recycle: |  |
|  | Gitea | :x: |  |
|  | Github | :x: |  |
|  | Gitlab | :x: |  |
|  | Kubernetes | :x: |  |

To find out what we are working on now please view the [Milestones](https://github.com/nofusscomputing/centurion_erp/milestones) on Github.
