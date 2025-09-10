---
title: Git Group
description: Git Group (DevOps) Module User Documentation for Centurion ERP by No Fuss Computing
date: 2025-03-20
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Git Groups are analogs to GitHub Organizations and GitLab Groups. To create a Git repository you will first need to create a git group.

!!! info
    This Feature is currently not available as it's still under development.


## Fields

- `parent_group` - The Parent Group for this group.

    !!! note
        GitHub does not have nested Organizations. Attempting to set this for a GitHub Group will fail to validate.

- `provider` - The Git Provider.

- `provider_id` - The Git Providers ID/Primary Key (PK).

- `name` - Friendly Name for this group.

- `path` - The path of this group.

- `description` Description for this group.
