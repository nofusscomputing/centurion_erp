## Verrsion 1.26.0


## Verrsion 1.25.0

- Centurion ERP relicenced to AGPL-3.0-only

- No end-user noticable features in this release. All new functionality is related to upcoming features.


## Version 1.24.1

- Fixed excessive query response times

## Version 1.24.0

- This release offered no and user feature, just middleware to enable optional tracing of Centurion Code for Administrators.

## Version 1.23.0

- Model Entity now available, as feature flag `2025-00002` has been removed from Centurion ERPs feature flag checks. The assosciated end user feature is [Contact Directory](https://nofusscomputing.com/projects/centurion_erp/user/access/contact/).


## Version 1.22.0

This release is an out of band release targeting the audit in [#980](https://github.com/nofusscomputing/centurion_erp/issues/980)


## Version 1.21.0

- Model [Roles](https://nofusscomputing.com/projects/centurion_erp/user/access/role/) now available, as feature flag `2025-00003` has been removed from Centurion ERPs feature flag checks.

- Model Teams **Removed**

    TL;DR
    _Teams were moved to roles so as to give the same authorization as was assigned under the teams based authorization._

    Teams moved to roles. As part of the migration, Each Teams permissions were moved to a role using the same name as the team the permissions came from. Notes from an team that contained them were also moved to the role. Users assigned to teams were added to a group that shares the name of the team and prefixed with `migrated-team-`. The group was also assigned to the role of the same name.

    !!! danger
        You are advised to conduct a thorough audit of the roles and groups to ensure they only provide the authorization that you intend to have assigned. Care was taking during development of the migration to assist with this, it may still be possible that the migration of authorization from teams to roles has made an error.


## Version 1.20.0

- New User model added.

    New model adds no end user features. Its intent is to consolidate the custom tenancy authorization for Centurion.


## Version 1.19.0

- Added new model for History

    !!! info
        Migration of the old history tables to the new history tables occurs as part of post migration. As such the time it will take to migrate the history is dependent upon how many history entries per model. This should be planned for when upgrading to this version. if for some reason the migration is interrupted, you can safely restart it again by running the migrate command.

    !!! note
        Permission migration from the old history models to the new Audit History models are not migrated. As such users whom used to be able to access history models will need to be granted the required permission to view the new Audit History models

- Added new model for notes

    !!! info
        Migration of the old notes tables to the new note tables occurs as part of post migration. As such the time it will take to migrate the history is dependent upon how many history entries per model. This should be planned for when upgrading to this version. if for some reason the migration is interrupted, you can safely restart it again by running the migrate command.

    !!! note
        Permission migration from the old history models to the new Centurion Notes models are not migrated. As such users whom used to be able to access notes models will need to be granted the required permission to view the new Centurion Notes models

- Removed Django UI

    [UI](https://github.com/nofusscomputing/centurion_erp_ui) must be deployed seperatly.

- Removed API v1


## Version 1.17.0

- Added setting for log files.

    Enables user to specify a default path for centurion's logging. Add the following to your settings file `/etc/itsm/settings.py`

    ``` py
    LOG_FILES = {
        "centurion": "/var/log/centurion.log",    # Normal Centurion Operations
        "weblog": "/var/log/weblog.log",          # All web requests made to Centurion
        "rest_api": "/var/log/rest_api.log",      # Rest API
        "catch_all":"/var/log/catch-all.log"      # A catch all log. Note: does not log anything that has already been logged.
    }

    ```

    With this new setting, the previous setting `LOGGING` will no longer function.

- Renamed `Organization` model to `Tenant` so as to reflect what is actually is.

- `robots.txt` file now being served from the API container at path `/robots.txt` with `User-agent: *` and `Disallow: /`


## Version 1.16.0

- Employees model added behind feature flag `2025-00002` and will remain behind this flag until production ready.

- Ticket and Ticket Comment added behind feature flag `2025-00006` and will remain behind this flag until production ready.

- In preparation of the [Ticket and Ticket Comment model re-write](https://github.com/nofusscomputing/centurion_erp/issues/564)

    - Depreciated Change Ticket

    - Depreciated Ticket Comment Endpoint

    - Depreciated Request Ticket

    - Depreciated Incident Ticket

    - Depreciated Problem Ticket

    - Depreciated Project Task Ticket

    These endpoints still work and will remain so until the new Ticket and Ticket Comment Models are production ready.


## Version 1.15.0

- Entities model added behind feature flag `2025-00002` and will remain behind this flag until production ready.

- Roles model added behind feature flag `2025-00003` and will remain behind this flag until production ready.

- Accounting Module added behind feature flag `2025-00004` and will remain behind this flag until production ready.


## Version 1.14.0

- Git Repository and Git Group Models added behind feature flag `2025-00001`. They will remain behind this feature flag until the Git features are fully developed and ready for use.


## Version 1.13.0

- DevOps Module added.

- Feature Flagging Component added as par of the DevOps module.


## Version 1.11.0

**Note:** Migrations should be performed offline. **Failing to perform** an online migration, the option provided below will not be available if the migration crashes. Running the below commands to reset the database for the migrations to re-run will cause data loss if users are making changes to Centurion.

- History views removed from original Centurion interface.

- History views removed from API v1.

- A migration exists that will move the history from the old tables to the new ones.

    if for some reason the migration crashes enter the following commands in the dbshell `python manage.py dbshell` and restart the migrations

    ``` sql

    delete from access_organization_history;
    delete from access_team_history;

    delete from assistance_knowledge_base_history;
    delete from assistance_knowledge_base_category_history;

    delete from config_management_configgroups_history;
    delete from config_management_configgroupsoftware_history;
    delete from config_management_configgrouphosts_history;

    delete from core_manufacturer_history;
    delete from core_ticketcategory_history;
    delete from core_ticketcommentcategory_history;
    
    delete from itam_device_history;
    delete from itam_devicemodel_history;
    delete from itam_devicetype_history;
    delete from itam_deviceoperatingsystem_history;
    delete from itam_devicesoftware_history;
    delete from itam_operatingsystem_history;
    delete from itam_operatingsystemversion_history;
    delete from itam_software_history;
    delete from itam_softwareversion_history;
    delete from itam_softwarecategory_history;

    delete from itim_cluster_history;
    delete from itim_clustertype_history;
    delete from itim_port_history;
    delete from itim_service_history;

    delete from project_management_project_history;
    delete from project_management_projectmilestone_history;
    delete from project_management_projectstate_history;
    delete from project_management_projecttype_history;
    delete from settings_externallink_history;

    delete from core_model_history;

    ```

    The above commands truncate the data from the new history tables so the migration can run again.


## Version 1.10.0

- Nothing significant to report


## Version 1.9.0

- Nothing significant to report


## Version 1.8.0

- Prometheus exporter added. To enable metrics for the database you will have to update the database backend. see the [docs](https://nofusscomputing.com/projects/centurion_erp/administration/monitoring/#django-exporter-setup) for further information.


## Version 1.5.0

- When v1.4.0 was release the migrations were not merged. As part of the work conducted on this release the v1.4 migrations have been squashed. This should not have any effect on any system that when they updated to v1.4, they ran the migrations and they **completed successfully**. Upgrading from <1.4.0 to this release should also have no difficulties as the migrations required still exist. There are less of them, however with more work per migration.

!!! Note
    If you require the previously squashed migrations for what ever reason. Clone the repo and go to commit 17f47040d6737905a1769eee5c45d9d15339fdbf, which is the commit prior to the squashing which is commit ca2da06d2cd393cabb7e172ad47dfb2dd922d952.


## Version 1.4.0

API redesign in preparation for moving the UI out of centurion to it's [own project](https://github.com/nofusscomputing/centurion_erp_ui). This release introduces a **Feature freeze** to the current UI. Only bug fixes will be done for the current UI.
API v2 is a beta release and is subject to change. On completion of the new UI, API v2 will more likely than not be set as stable.

- A large emphasis is being placed upon API stability. This is being achieved by ensuring the following:

    - Actions can only be carried out by users whom have the correct permissions

    - fields are of the correct type and visible when required as part of the API response

    - Data validations work and notify the user of any issue

    We are make the above possible by ensuring a more stringent test policy.

- New API will be at path `api/v2`.

- API v1 is now **Feature frozen** with only bug fixes being completed. It's recommended that you move to and start using API v2 as this has feature parity with API v1.

- API v1 is **depreciated**

- Depreciation of **ALL** API urls. API v1 Will be [removed in v2.0.0](https://github.com/nofusscomputing/centurion_erp/issues/343) release of Centurion.


# Version 1.3.0

!!! danger "Security"
    As is currently the recommended method of deployment, the Centurion Container must be deployed behind a reverse proxy the conducts the SSL termination.

This release updates the docker container to be a production setup for deployment of Centurion. Prior to this version Centurion ERP was using a development setup for the webserver.

- Docker now uses SupervisorD for container

- Gunicorn WSGI setup for Centurion with NginX as the webserver.

- Container now has a health check.

- To setup container as "Worker", set `IS_WORKER='True'` environmental variable within container. _**Note:** You can still use command `celery -A app worker -l INFO`, although **not** recommended as the container health check will not be functioning_


## Version 1.0.0


Initial Release of Centurion ERP.


### Breaking changes

- Nil
