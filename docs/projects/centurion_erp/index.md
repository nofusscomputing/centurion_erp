---
title: Centurion ERP
description: Documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

<span style="text-align: center;">

![Project Status](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2Fcenturion_erp%2Frefs%2Fheads%2Fdevelopment%2F.centurion%2Fproject_status.json)

![Docker Pulls](https://img.shields.io/docker/pulls/nofusscomputing/centurion-erp?style=plastic&logo=docker&color=0db7ed) [![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/centurion-erp)](https://artifacthub.io/packages/container/centurion-erp/centurion-erp)

![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Frefs%2Fheads%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fmaster%2Fbadge_endpoint_integration_postgres_versions.json&style=plastic&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iNDMyLjA3MXB0IiBoZWlnaHQ9IjQ0NS4zODNwdCIgdmlld0JveD0iMCAwIDQzMi4wNzEgNDQ1LjM4MyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgaWQ9Im9yZ2luYWwiIHN0eWxlPSJmaWxsLXJ1bGU6bm9uemVybztjbGlwLXJ1bGU6bm9uemVybztzdHJva2U6IzAwMDAwMDtzdHJva2UtbWl0ZXJsaW1pdDo0OyI%2BCgk8L2c%2BCjxnIGlkPSJMYXllcl94MDAyMF8zIiBzdHlsZT0iZmlsbC1ydWxlOm5vbnplcm87Y2xpcC1ydWxlOm5vbnplcm87ZmlsbDpub25lO3N0cm9rZTojRkZGRkZGO3N0cm9rZS13aWR0aDoxMi40NjUxO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2UtbWl0ZXJsaW1pdDo0OyI%2BCjxwYXRoIHN0eWxlPSJmaWxsOiMwMDAwMDA7c3Ryb2tlOiMwMDAwMDA7c3Ryb2tlLXdpZHRoOjM3LjM5NTM7c3Ryb2tlLWxpbmVjYXA6YnV0dDtzdHJva2UtbGluZWpvaW46bWl0ZXI7IiBkPSJNMzIzLjIwNSwzMjQuMjI3YzIuODMzLTIzLjYwMSwxLjk4NC0yNy4wNjIsMTkuNTYzLTIzLjIzOWw0LjQ2MywwLjM5MmMxMy41MTcsMC42MTUsMzEuMTk5LTIuMTc0LDQxLjU4Ny03YzIyLjM2Mi0xMC4zNzYsMzUuNjIyLTI3LjcsMTMuNTcyLTIzLjE0OGMtNTAuMjk3LDEwLjM3Ni01My43NTUtNi42NTUtNTMuNzU1LTYuNjU1YzUzLjExMS03OC44MDMsNzUuMzEzLTE3OC44MzYsNTYuMTQ5LTIwMy4zMjIgICAgQzM1Mi41MTQtNS41MzQsMjYyLjAzNiwyNi4wNDksMjYwLjUyMiwyNi44NjlsLTAuNDgyLDAuMDg5Yy05LjkzOC0yLjA2Mi0yMS4wNi0zLjI5NC0zMy41NTQtMy40OTZjLTIyLjc2MS0wLjM3NC00MC4wMzIsNS45NjctNTMuMTMzLDE1LjkwNGMwLDAtMTYxLjQwOC02Ni40OTgtMTUzLjg5OSw4My42MjhjMS41OTcsMzEuOTM2LDQ1Ljc3NywyNDEuNjU1LDk4LjQ3LDE3OC4zMSAgICBjMTkuMjU5LTIzLjE2MywzNy44NzEtNDIuNzQ4LDM3Ljg3MS00Mi43NDhjOS4yNDIsNi4xNCwyMC4zMDcsOS4yNzIsMzEuOTEyLDguMTQ3bDAuODk3LTAuNzY1Yy0wLjI4MSwyLjg3Ni0wLjE1Nyw1LjY4OSwwLjM1OSw5LjAxOWMtMTMuNTcyLDE1LjE2Ny05LjU4NCwxNy44My0zNi43MjMsMjMuNDE2Yy0yNy40NTcsNS42NTktMTEuMzI2LDE1LjczNC0wLjc5NywxOC4zNjdjMTIuNzY4LDMuMTkzLDQyLjMwNSw3LjcxNiw2Mi4yNjgtMjAuMjI0ICAgIGwtMC43OTUsMy4xODhjNS4zMjUsNC4yNiw0Ljk2NSwzMC42MTksNS43Miw0OS40NTJjMC43NTYsMTguODM0LDIuMDE3LDM2LjQwOSw1Ljg1Niw0Ni43NzFjMy44MzksMTAuMzYsOC4zNjksMzcuMDUsNDQuMDM2LDI5LjQwNmMyOS44MDktNi4zODgsNTIuNi0xNS41ODIsNTQuNjc3LTEwMS4xMDciLz4KPHBhdGggc3R5bGU9ImZpbGw6IzMzNjc5MTtzdHJva2U6bm9uZTsiIGQ9Ik00MDIuMzk1LDI3MS4yM2MtNTAuMzAyLDEwLjM3Ni01My43Ni02LjY1NS01My43Ni02LjY1NWM1My4xMTEtNzguODA4LDc1LjMxMy0xNzguODQzLDU2LjE1My0yMDMuMzI2Yy01Mi4yNy02Ni43ODUtMTQyLjc1Mi0zNS4yLTE0NC4yNjItMzQuMzhsLTAuNDg2LDAuMDg3Yy05LjkzOC0yLjA2My0yMS4wNi0zLjI5Mi0zMy41Ni0zLjQ5NmMtMjIuNzYxLTAuMzczLTQwLjAyNiw1Ljk2Ny01My4xMjcsMTUuOTAyICAgIGMwLDAtMTYxLjQxMS02Ni40OTUtMTUzLjkwNCw4My42M2MxLjU5NywzMS45MzgsNDUuNzc2LDI0MS42NTcsOTguNDcxLDE3OC4zMTJjMTkuMjYtMjMuMTYzLDM3Ljg2OS00Mi43NDgsMzcuODY5LTQyLjc0OGM5LjI0Myw2LjE0LDIwLjMwOCw5LjI3MiwzMS45MDgsOC4xNDdsMC45MDEtMC43NjVjLTAuMjgsMi44NzYtMC4xNTIsNS42ODksMC4zNjEsOS4wMTljLTEzLjU3NSwxNS4xNjctOS41ODYsMTcuODMtMzYuNzIzLDIzLjQxNiAgICBjLTI3LjQ1OSw1LjY1OS0xMS4zMjgsMTUuNzM0LTAuNzk2LDE4LjM2N2MxMi43NjgsMy4xOTMsNDIuMzA3LDcuNzE2LDYyLjI2Ni0yMC4yMjRsLTAuNzk2LDMuMTg4YzUuMzE5LDQuMjYsOS4wNTQsMjcuNzExLDguNDI4LDQ4Ljk2OWMtMC42MjYsMjEuMjU5LTEuMDQ0LDM1Ljg1NCwzLjE0Nyw0Ny4yNTRjNC4xOTEsMTEuNCw4LjM2OCwzNy4wNSw0NC4wNDIsMjkuNDA2YzI5LjgwOS02LjM4OCw0NS4yNTYtMjIuOTQyLDQ3LjQwNS01MC41NTUgICAgYzEuNTI1LTE5LjYzMSw0Ljk3Ni0xNi43MjksNS4xOTQtMzQuMjhsMi43NjgtOC4zMDljMy4xOTItMjYuNjExLDAuNTA3LTM1LjE5NiwxOC44NzItMzEuMjAzbDQuNDYzLDAuMzkyYzEzLjUxNywwLjYxNSwzMS4yMDgtMi4xNzQsNDEuNTkxLTdjMjIuMzU4LTEwLjM3NiwzNS42MTgtMjcuNywxMy41NzMtMjMuMTQ4eiIvPgo8cGF0aCBkPSJNMjE1Ljg2NiwyODYuNDg0Yy0xLjM4NSw0OS41MTYsMC4zNDgsOTkuMzc3LDUuMTkzLDExMS40OTVjNC44NDgsMTIuMTE4LDE1LjIyMywzNS42ODgsNTAuOSwyOC4wNDVjMjkuODA2LTYuMzksNDAuNjUxLTE4Ljc1Niw0NS4zNTctNDYuMDUxYzMuNDY2LTIwLjA4MiwxMC4xNDgtNzUuODU0LDExLjAwNS04Ny4yODEiLz4KPHBhdGggZD0iTTE3My4xMDQsMzguMjU2YzAsMC0xNjEuNTIxLTY2LjAxNi0xNTQuMDEyLDg0LjEwOWMxLjU5NywzMS45MzgsNDUuNzc5LDI0MS42NjQsOTguNDczLDE3OC4zMTZjMTkuMjU2LTIzLjE2NiwzNi42NzEtNDEuMzM1LDM2LjY3MS00MS4zMzUiLz4KPHBhdGggZD0iTTI2MC4zNDksMjYuMjA3Yy01LjU5MSwxLjc1Myw4OS44NDgtMzQuODg5LDE0NC4wODcsMzQuNDE3YzE5LjE1OSwyNC40ODQtMy4wNDMsMTI0LjUxOS01Ni4xNTMsMjAzLjMyOSIvPgo8cGF0aCBzdHlsZT0ic3Ryb2tlLWxpbmVqb2luOmJldmVsOyIgZD0iTTM0OC4yODIsMjYzLjk1M2MwLDAsMy40NjEsMTcuMDM2LDUzLjc2NCw2LjY1M2MyMi4wNC00LjU1Miw4Ljc3NiwxMi43NzQtMTMuNTc3LDIzLjE1NWMtMTguMzQ1LDguNTE0LTU5LjQ3NCwxMC42OTYtNjAuMTQ2LTEuMDY5Yy0xLjcyOS0zMC4zNTUsMjEuNjQ3LTIxLjEzMywxOS45Ni0yOC43MzljLTEuNTI1LTYuODUtMTEuOTc5LTEzLjU3My0xOC44OTQtMzAuMzM4ICAgIGMtNi4wMzctMTQuNjMzLTgyLjc5Ni0xMjYuODQ5LDIxLjI4Ny0xMTAuMTgzYzMuODEzLTAuNzg5LTI3LjE0Ni05OS4wMDItMTI0LjU1My0xMDAuNTk5Yy05Ny4zODUtMS41OTctOTQuMTksMTE5Ljc2Mi05NC4xOSwxMTkuNzYyIi8%2BCjxwYXRoIGQ9Ik0xODguNjA0LDI3NC4zMzRjLTEzLjU3NywxNS4xNjYtOS41ODQsMTcuODI5LTM2LjcyMywyMy40MTdjLTI3LjQ1OSw1LjY2LTExLjMyNiwxNS43MzMtMC43OTcsMTguMzY1YzEyLjc2OCwzLjE5NSw0Mi4zMDcsNy43MTgsNjIuMjY2LTIwLjIyOWM2LjA3OC04LjUwOS0wLjAzNi0yMi4wODYtOC4zODUtMjUuNTQ3Yy00LjAzNC0xLjY3MS05LjQyOC0zLjc2NS0xNi4zNjEsMy45OTR6Ii8%2BCjxwYXRoIGQ9Ik0xODcuNzE1LDI3NC4wNjljLTEuMzY4LTguOTE3LDIuOTMtMTkuNTI4LDcuNTM2LTMxLjk0MmM2LjkyMi0xOC42MjYsMjIuODkzLTM3LjI1NSwxMC4xMTctOTYuMzM5Yy05LjUyMy00NC4wMjktNzMuMzk2LTkuMTYzLTczLjQzNi0zLjE5M2MtMC4wMzksNS45NjgsMi44ODksMzAuMjYtMS4wNjcsNTguNTQ4Yy01LjE2MiwzNi45MTMsMjMuNDg4LDY4LjEzMiw1Ni40NzksNjQuOTM4Ii8%2BCjxwYXRoIHN0eWxlPSJmaWxsOiNGRkZGRkY7c3Ryb2tlLXdpZHRoOjQuMTU1O3N0cm9rZS1saW5lY2FwOmJ1dHQ7c3Ryb2tlLWxpbmVqb2luOm1pdGVyOyIgZD0iTTE3Mi41MTcsMTQxLjdjLTAuMjg4LDIuMDM5LDMuNzMzLDcuNDgsOC45NzYsOC4yMDdjNS4yMzQsMC43Myw5LjcxNC0zLjUyMiw5Ljk5OC01LjU1OWMwLjI4NC0yLjAzOS0zLjczMi00LjI4NS04Ljk3Ny01LjAxNWMtNS4yMzctMC43MzEtOS43MTksMC4zMzMtOS45OTYsMi4zNjd6Ii8%2BCjxwYXRoIHN0eWxlPSJmaWxsOiNGRkZGRkY7c3Ryb2tlLXdpZHRoOjIuMDc3NTtzdHJva2UtbGluZWNhcDpidXR0O3N0cm9rZS1saW5lam9pbjptaXRlcjsiIGQ9Ik0zMzEuOTQxLDEzNy41NDNjMC4yODQsMi4wMzktMy43MzIsNy40OC04Ljk3Niw4LjIwN2MtNS4yMzgsMC43My05LjcxOC0zLjUyMi0xMC4wMDUtNS41NTljLTAuMjc3LTIuMDM5LDMuNzQtNC4yODUsOC45NzktNS4wMTVjNS4yMzktMC43Myw5LjcxOCwwLjMzMywxMC4wMDIsMi4zNjh6Ii8%2BCjxwYXRoIGQ9Ik0zNTAuNjc2LDEyMy40MzJjMC44NjMsMTUuOTk0LTMuNDQ1LDI2Ljg4OC0zLjk4OCw0My45MTRjLTAuODA0LDI0Ljc0OCwxMS43OTksNTMuMDc0LTcuMTkxLDgxLjQzNSIvPgo8cGF0aCBzdHlsZT0ic3Ryb2tlLXdpZHRoOjM7IiBkPSJNMCw2MC4yMzIiLz4KPC9nPgo8L3N2Zz4K)
 ![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Frefs%2Fheads%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fmaster%2Fbadge_endpoint_integration_rabbitmq_versions.json&style=plastic)

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nofusscomputing/centurion_erp/ci.yaml?branch=master&style=plastic&logo=github&label=Stable%20Build&color=%23000) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nofusscomputing/centurion_erp/ci.yaml?branch=development&style=plastic&logo=github&label=Dev%20Build&color=%23000)

![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/nofusscomputing/centurion_erp?style=plastic&logo=github&label=Open%20Issues&color=000) ![GitHub issue bugs](https://img.shields.io/github/issues-search?query=repo%3Anofusscomputing%2Fcenturion_erp%20type%3A%22Bug%22%20is%3Aopen%20&style=plastic&logo=github&label=Bug%20fixes%20required&color=000)

![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fdevelopment%2Fbadge_endpoint_coverage.json&style=plastic) ![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fdevelopment%2Fbadge_endpoint_unit_test.json)

![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fmaster%2Fbadge_endpoint_coverage_functional.json&style=plastic)
 ![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fmaster%2Fbadge_endpoint_functional_test.json)


</span>

<!-- markdownlint-disable no-emphasis-as-heading -->
_"`An ERP with a large emphasis on the IT Service Management (ITSM) and Automation."_
<!-- markdownlint-restore -->

Whilst there are many Enterprise Rescource Planning (ERP) applications, most suffer one or more of the following issues:

- High upfront and hidden costs
- Critical features locked behind paywalls
- Complex, bloated deployments that overwhelm smaller teams
- Poor usability and steep learning curves that frustrate staff
- Painful integrations and migration headaches
- Ongoing maintenance costs and technical debt

Centurion ERP is developed as a community project, a true open source product with no restrictions or hidden tiers. It is not an “open core” model with premium features locked away, nor a downstream edition of a paid product. Everything Centurion ERP offers is freely available to everyone. Centurion ERP allows users to adopt functionality at their own pace, avoiding unnecessary complexity. Centurion ERP is designed to include all the software features a user needs within a single platform, enabling true consolidation and reducing reliance on multiple external systems; where a specific feature is missing, the system can be easily extended to fill the gap.

By addressing these common challenges directly, Centurion ERP aims to provide a practical, sustainable ERP that supports growth without introducing unnecessary barriers.

!!! quote "From the creator:"
    An ERP, depending on industry; can have a lot of modules. This equates to a lot of time to design and implement--Reality is, I'm a single person and as such will not be able to add a lot of features due to that fact. This is not an intent that Centurion ERP will not have those modules/features added/created. In this circumstance it will be left up to the community to implement. With that said, my focus is to provide a system that is not only an IT Infrastructure Library (ITIL), but that of which will connect to other ITSM systems, i.e. AWX for automation orchestration. In addition, also provide the base modules to Centurion ERP so that it can be easily extended with the required features that one would find within an ERP.


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

| Area | Feature | Status | Notes |
|:---|:---|:---:|:---|
| **[Accounting](./user/accounting/index.md)** ||| _[see #88](https://github.com/nofusscomputing/centurion_erp/issues/88)_ |
| | Accounts Payable | :x: |  |
| | Accounts Receivable | :x: |  |
| | Asset Management | :recycle: | _[see #89](https://github.com/nofusscomputing/centurion_erp/issues/88)_ |
| | Budgeting & Forecasting | :x: |  |
| | Cash Management | :x: |  |
| | Cost Center Management | :x: |  |
| | Expense Management | :x: |  |
| | Financial Reporting & Analytics | :x: |  |
| | General Ledger | :x: | [see #116](https://github.com/nofusscomputing/centurion_erp/issues/116) |
| | Income Management | :x: |  |
| | Investment Management | :x: |  |
| | Tax Management | :x: |  |
| **Core** |  |  |  |
| | [API](./user/api.md) | :white_check_mark: |  |
| | [Application wide settings](./user/settings/app_settings.md) | :white_check_mark: |  |
| | [Audit History](./user/core/audit_history.md) | :white_check_mark: |  |
| | [Corporate Directory (contacts)](./user/access/contact.md) | :white_check_mark: | _[see #705](https://github.com/nofusscomputing/centurion_erp/issues/705)_ |
| | Location Management (Regions, Sites and Locations) | :x: | _[see #62](https://github.com/nofusscomputing/centurion_erp/issues/62)_ |
| | [Markdown](./user/core/markdown.md) | :white_check_mark: |  |
| | [Multi-Tenant](./user/access/tenant.md) | :white_check_mark: |  |
| | [Roles (RBAC)](./user/access/role.md) | :white_check_mark: |  |
| | [Single Sign-On {SSO}](./user/configuration.md#single-sign-on) | :white_check_mark: |  |
| | Soft Deleting | :x: |  |
| **Customer Relationship Management (CRM)** || :x: | _[see #91](https://github.com/nofusscomputing/centurion_erp/issues/91)_  |
| | Customers | :x: |  |
| | Field Service Management | :x: |  |
| | Invoice Management | :x: |  |
| | Pricing & Discounts | :x: |  |
| | Quote & Proposal Management | :x: |  |
| | Returns & Claims Management | :x: |  |
| | Sales Order Management | :x: |  |
| **[Development Operations (DevOps)](./user/devops/index.md)**  ||| _[see #68](https://github.com/nofusscomputing/centurion_erp/issues/58)_ |
| | [Feature Flag Management](./user/devops/feature_flags.md) | :white_check_mark: |  |
| | Test Management | :x: |  |
| | Release Management | :x: |  |
| | [Repository Management](./user/devops/git_repository.md) | :recycle: | _[see #115](https://github.com/nofusscomputing/centurion_erp/issues/115)_ |
| | Requirements Management | :x: |  |
| | Version Control / Source Code Management | :x: |  |
| | Public Repository Management | :x: | _[see #998](https://github.com/nofusscomputing/centurion_erp/issues/998)_ |
| Facilities Management ||| _[see #574](https://github.com/nofusscomputing/centurion_erp/issues/574)_ |
| | Building Management | :x: |  |
| | Maintenence Management | :x: |  |
| | Room Management | :x: |  |
| Fleet Management |||  |
| | Vehicle Management | :x: |  |
| **[Human Resource Management](./user/human_resources/index.md)**  || :recycle: | [see #92](https://github.com/nofusscomputing/centurion_erp/issues/92) |
| | [Employee Records](./user/human_resources/employee.md) | :recycle: |  |
| | Maintenence Management | :x: |  |
| | Onboarding / Offboarding | :x: |  |
| | Self-Service | :x: |  |
| Idea & Innovation Management || :x: |  |
| | Idea Capture / Submission | :x: |  |
| IT Infrastructure Management (ITIM)<br>Data Center Infrastructure Management (DCIM) |||  |
| | Bare Metal Provisioning | :x: |  |
| | BMC Server Management | :x: |  |
| | Cable Management | :x: |  |
| | Capacity Planning | :x: |  |
| | [Cluster Management](./user/itim/cluster.md) | :recycle: |  |
| | Rack Management | :x: |  |
| | [Service Management](./user/itim/service.md) | :white_check_mark: |  |
| | User Provisioning / De-provisioning | :x: |  |
| | Virtual Machine Management | :x: | _[see #73](https://github.com/nofusscomputing/centurion_erp/issues/73)_ |
| IT Service Management (ITSM / ITIL) |||  |
| | Certificate Management | :x: |  |
| | Change Management | :recycle: | _[see #90](https://github.com/nofusscomputing/centurion_erp/issues/90)_ |
| | [Configuration Management](./user/config_management/index.md) | :white_check_mark: |  |
| | Database Management | :x: | _[see #72](https://github.com/nofusscomputing/centurion_erp/issues/72)_ |
| | Incident Management | :recycle: | _[see #93](https://github.com/nofusscomputing/centurion_erp/issues/93)_ |
| | [IT Asset Management (ITAM)](./user/itam/index.md) | :white_check_mark: |  |
| | [Knowledge Base](./user/assistance/knowledge_base.md) | :white_check_mark: |  |
| | Licence Management | :x: | _[see #4](https://github.com/nofusscomputing/centurion_erp/issues/4)_ |
| | [OS Asset Management (OAM)](./user/itam/operating_system.md) | :white_check_mark: | |
| | Problem Management | :recycle: | _[see #95](https://github.com/nofusscomputing/centurion_erp/issues/95)_ |
| | Release and Deployment Management | :x: | _[see #462](https://github.com/nofusscomputing/centurion_erp/issues/462)_ |
| | Service Catalog | :x: | _[see #384](https://github.com/nofusscomputing/centurion_erp/issues/384)_ |
| | Service Level Management  | :x: | _[see #396](https://github.com/nofusscomputing/centurion_erp/issues/396)_ |
| | Service Request Management | :recycle: | _[see #96](https://github.com/nofusscomputing/centurion_erp/issues/96)_ |
| | [Software Asset Management (SAM)](./user/itam/software.md) | :white_check_mark: |  |
| | Software Package Management | :x: | _[see #96](https://github.com/nofusscomputing/centurion_erp/issues/96)_ |
| | User Access & Roles | :x: |  _[see #70](https://github.com/nofusscomputing/centurion_erp/issues/70)_ |
| | Vulnerability Management | :x: | _[see #3](https://github.com/nofusscomputing/centurion_erp/issues/3)_ |
| | Workflow Automation | :x: | _Possibly going to be done as integration with EDA Server and AWX_ |
| **[Project Management](./user/project_management/index.md)** |||  |
| | [Milestones](./user/project_management/project.md#milestones) | :white_check_mark: |  |
| | [Projects](./user/project_management/project.md) | :white_check_mark: |  |
| | Roadmap | :x: |  |
| | [Tasks](./user/project_management/project_task.md) | :recycle: |  |
| Supply Chain Management (SCM) |||  |
| | Contract Management | :x: |  |
| | Purchase Requisition & Order | :x: | _[see #94](https://github.com/nofusscomputing/centurion_erp/issues/94)_ |
| | Supplier Management | :x: |  _[see #123](https://github.com/nofusscomputing/centurion_erp/issues/123)_ |
| | Inventory Management | :x: |  |
| | Purchase Invoice Management | :x: |  |
| **Third party Integrations** |||  |
| | ArgoCD | :x: | [ArgoCD](https://github.com/argoproj-labs) is a Continuous Deployment system for ensuring objects deployed to kubernetes remain in the desired state. _[see #77](https://github.com/nofusscomputing/centurion_erp/issues/77)_ |
| | AWX | :x: | [AWX](https://github.com/ansible/awx) is an Automation Orchestration system that uses Ansible for its configuration. _[see #113](https://github.com/nofusscomputing/centurion_erp/issues/113)_ |
| | [Companion Ansible Collection](../ansible/collection/centurion/index.md) | :recycle: |  |
| | Gitea | :x: |  |
| | Github | :recycle: |  |
| | Gitlab | :recycle: |  |
| | Kubernetes | :x: |  _[see #999](https://github.com/nofusscomputing/centurion_erp/issues/999)_ |

To find out what we are working on now please view the [Milestones](https://github.com/nofusscomputing/centurion_erp/milestones) on Github.


## Licencing

Centurion ERP is released under the GNU Affero General Public License (AGPL-3.0-only).

The AGPL guarantees full access to the source code, with the freedom to use, modify, and extend the system as needed. Unlike other licenses, the AGPL ensures that improvements made are shared back with the community. This protects users from vendor lock-in and ensures that Centurion ERP remains transparent, auditable, and community-driven over the long term.

A common concern with this and similar licences, is the idea of “having to share code.” This often causes confusion and leads decision makers to opt away from using software with these conditions. This confusion generally stems from a lack of understanding of what the "sharing code" means. Simply put, any modification that is made to Centurion, not your data (which is anything you enter into Centurion ERP once it's installed); is what is shared with the community. This condition in particular enforces that any improvements anyone makes then become available for everyone, strengthening Centurion ERP as a product.

Finally, if Centurion’s licence were ever changed to something more restrictive, the community can always fork the last AGPL release. This safeguard ensures that Centurion ERP — or its successor forks — will always remain free and open.


!!! example
    Company ACME has decided to use Centurion ERP. They are a manufacturing company. Centurion is missing the manufacturing features. So company ACME requires a software developer (or someone skilled enough) to extend Centurion ERP with the features required. ACME then deploys Centurion ERP with the features they added to Centurion ERP. In addition, **ALL** of the work the software developer does "must" be publically available (AGPL requirement).

    Now company Homewares comes along whom is also a manufacturer. They see that Centurion ERP has the manufacturing features, thanks to ACME company. However in this case, Homewares company wants to add additional features. to do this they fork ACME companies work and add the new features. Again they share all of the work they did.

    Now there are two different manufacturing "feature sets". ACME can if they choose, use Homewares manufacturing "features" or they can stick to their own, which also incldues ONLY extending their own manufacturing "features".
