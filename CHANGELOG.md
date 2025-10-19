## 1.26.1 (2025-10-19)

### Refactoring

- **human_resources**: Adjust employee id field, int -> bigint

## 1.26.0 (2025-10-18)

### feat

- **core**: When a ticket comment is created, associate with currently authenticated user
- **core**: ensure that when attempting to link sub-model reqs are met
- **human_resources**: Add user field to Employee details page
- **human_resources**: Add Migration signal to ensure that all users have an Employy entity created.
- **core**: Add Linking of parent models when sub-model is being created
- **human_resources**: Migration for field user to Employee Entity model
- **human_resources**: Add field user to Employee Entity model
- **human_resources**: remove feature flag 2025-00005

### Fixes

- **core**: Whn attempting to link a model, if it already has an id, dont attempt to link to a parent
- **human_resources**: when adding users as an employee as part of migration signal auto-generate the names if hey are blank
- **access**: Entity qs must e cached
- **itam**: Oranizatio field must be null if not defined for Software model
- **core**: When validating a ticket comment always set its tenancy to the tickets tenancy
- **core**: when saving a model if no before data is found (`=None`) set to empty dict by default
- **access**: when fetching data, determine type by model
- **core**: When fetching model history during save, when no pk exists, always assume creatung model
- **access**: Contacts must be filtered to those who opt for directory listing
- **access**: when setting display name for entiry models, use get_related_model function

### Refactoring

- **core**: When generating entity display name, look in the entity type class for it first
- **core**: migrations for TicketBase field to be Entity model
- **core**: migrate opened_by field to be Entity model
- **access**: organization field must be null for tenancy_abstract_model
- **core**: update get_url functions to use get_related_model function
- migrate function get_related_model to Centurion mixin
- migrate function get_related_field_name to Centurion mixin

### Tests

- **base**: Functional test cases to ensure that when creating and edting a model that the supplied data matches what's saved
- **core**: Ensure ticket comment cant be created if the user has no entity assigned
- **core**: Ensure ticket cant be created if the user has no entity assigned
- **access**: Test cases to ensure that child model links to existing person model
- **access**: Test cases to ensure that child model links to existing contact model
- **access**: remove test for validation of duplicate
- **human_resources**: Update Test suites for employee to perform fiels User checks
- **core**: Remove centrion mixin function test to check returning related model name
- **human_resources**: Unit ViewSet test suite for Employee model
- **human_resources**: Unit serializer test suite for Employee model
- **human_resources**: Functional model test suite for Employee model

## 1.25.0 (2025-10-10)

### feat

- **python**: update social-auth-app-django 5.4.1 -> 5.6.0
- **python**: Upgrade django 5.1.12 -> 5.1.13
- **base**: prevent python depreciation warnings within the docker container
- **core**: add model manager ModelTicket
- **core**: Add new method for processing link slash command
- **core**: enable posting to modelticket endpoint
- Add field `model` to modelticket setializers
- **core**: Make  model core.ModelTicketMetaModel so ticket only assigned once
- **core**: Add URL Route for model core.ModelTicketMetaModel
- **core**: Add URL Route for model core.ModelTicket again
- **core**: order model ModelTicket by created date
- **core**: Add Migrations for model core.ModelTicket
- **core**: Add URL Route for model core.ModelTicket
- **core**: Add ViewSet for model core.ModelTicket
- **core**: Add serializer for model core.ModelTicket
- **core**: Add new model core.ModelTicket
- **core**: Do not allow a ticket comment to be deleted when it has threads
- **core**: Add TicketBase model permissions import, purge and triage

### Fixes

- **core**: Ensure model_type=tenant selects the right type
- **core**: when validating ModelTicket uniqueness, exclude self
- **core**: Correct model field name and description for ModelTicket
- ModelTicket sub-Serializers require field `ticket` be writable
- **api**: when converting viewset exception, check msg attr exists
- **core**: TicketModel ViewSerializer to inherit from bas ViewSerializer
- **core**: ret model_suffix to ViewSet
- **core**: Field change detection for ticket must cater for foriegn field ids
- **core**: When adding a comment of TicketCommentSolution, it must solve the ticket
- **core**: Add delete method to TicketCommentBase
- **core**: TicketCommentBase model method clean must call super
- **settings**: AppSettings model method clean must call super
- **itim**: Service model method clean must call super
- **itam**: Software model method clean must call super
- **itam**: SoftwareCategory model method clean must call super
- **itam**: DeviceType model method clean must call super
- **itam**: DeviceModel model method clean must call super
- **core**: TicketBase model method clean must call super
- **core**: Manufacturer model method clean must call super

### Refactoring

- **core**: move ticket sub url so it's fully-dynamic

### Tests

- **core**: Unit Test cases for ModelTicket Serializer Validate method
- **core**: Unit Test cases for ModelTicket Serializer Validate method
- **core**: ModelTicket Manager Test Suite
- refactor fixtures to fixture factories
- **api**: Ensure when checking queryset filtered results all of the test data is available.
- **core**: Add functional model test to ensure ticket and model can only be assigned once
- **core**: Add functional ViewSet Test suite for ALL ModelTickets models
- **core**: Add functional Model Test suite for ALL ModelTickets models
- **core**: Add functional API Permissions Test suite for ALL ModelTickets endpoints
- **core**: Add API Fields REnder Functional Test suites for model ModelTicket
- **core**: Add ViewSet Unit test suite for model ModelTicketMetaModels
- **core**: Add Serializer Unit test suite for model ModelTicketMetaModels again
- **core**: Add Serializer Unit test suite for model ModelTicketMetaModels
- **core**: Add Serializer Unit test suite for model ModelTicketMeta
- **core**: Add Model Unit test suite for model ModelTicketMetaModels
- **core**: Add Model Unit test suite for model ModelTicketMetaModel
- **core**: Correct Serializer Unit test case for model ModelTicket is_valid
- **core**: Add Serializer Unit test suite for model ModelTicket
- **core**: Add ViewSet Unit test suite for model ModelTicket
- **core**: Add Unit test case for model attribute `_ticket_linkable`
- **core**: Add Unit test suite for model ModelTicket
- **core**: Add TicketCommentAction Unit Serializer test suite
- **core**: Add TicketCommentSolution Unit Serializer test suite
- **core**: Add TicketCommentSolution functional ViewSet test suite
- **core**: Add TicketCommentAction functional ViewSer test suite
- **core**: Add TicketCommentSolution functional model test cases for threads
- **core**: Add TicketCommentAction functional model test cases for threads
- **core**: Add TicketBaseComment functional model test cases for threads
- **core**: Update TicketCommentSolution unit model test suite
- **core**: Update TicketCommentSolution unit ViewSet test suite
- **core**: Update TicketCommentAction unit ViewSet test suite
- **core**: Update TicketCommentBase unit ViewSet test suite
- **core**: Add TicketCommentBase unit Serializer test suite
- **itim**: Remove skip for TicketCommentBase unit model test suite
- **itim**: Add TicketCommentBase functional ViewSet test suite
- **itim**: Remove skip for TicketCommentBase Functional api_fields test suite
- **itim**: add RequestTicket Functional model test suite
- **itim**: add SLMTicket Functional model test suite
- **core**: skip clean_fields method super call test case as model is abstract for model MetaAbstract Note
- **core**: skip clean_fields method super call test case as model is abstract for model MetaAbstract Audit
- Add test cases to unit Model test suite for all model clean fields methods along inheritance chain
- **core**: Add sub-Model unit test cases for model TicketBase
- **core**: Model functional test cases for model TicketBase clean function
- **itim**: Update viewset functional test suite for model RequestTicket
- **itim**: Update viewset functional test suite for model SLMTicket
- **core**: Update viewset functional test suite for model TicketBase
- **core**: Update metadata functional test suite for model TicketBase
- **core**: Model unit test case for model TicketBase checking milstone choices
- **core**: Re-Enable Model unit test suit for model TicketBase
- **core**: Add ViewSet unit test suit for model TicketBase
- **itim**: Add ViewSet unit test suit for model SLMTicket
- **itim**: Add Serializer unit test suit for model SLMTicket
- **itim**: Add ViewSet unit test suit for model RequestTicket
- **itim**: Add Serializer unit test suit for model RequestTicket
- **core**: Add ViewSet unit test suit for model TicketBase
- **core**: Add Serializer unit test suit for model TicketBase

## 1.24.1 (2025-09-17)

### Fixes

- **base**: remove gunicorn syslog address
- **feature_flag**: when fetching a feature flag and it's not enabled, ALWAYS return false
- **base**: gunicorn logging config setup
- **feature_flag**: use get to fetch a potentially empty dict
- **base**: Dont add syslog handler when no address is supplied

### Refactoring

- **base**: set gunicorn to only log errors
- **base**: configure handlers for error log
- **base**: Move supervisor app logs to own dir for clarity
- **base**: Log ALL errors to own file in addition to specified log
- **base**: Add logging levels to base class

### Tests

- **devops**: Ensure that feature flags are not obtained during HTTP request processing

## 1.24.0 (2025-09-13)

### feat

- **base**: Add Optional Trace Debugging to Centurion

## 1.23.0 (2025-09-10)

### feat

- **base**: Upgrade Django 5.1.10 -> 5.1.12
- **access**: Remove feature flag 2025-00002

### Tests

- **access**: Add Model functional test suit for model Person
- **access**: Add Model functional test suit for model Entity
- **access**: Add Model functional test suit for model Contact
- **access**: Add Serializer unit test suit for model Contact
- **access**: Add Serializer unit test suit for model Person
- **access**: Add Serializer unit test suit for model Entity

## 1.22.0 (2025-09-09)

### feat

- **access**: Add global tenancy to user object
- **access**: Add superuser viewset permissions
- **access**: Add tenancy manager to Tenant model
- **access**: User based model permissions and model Manager
- **api**: TenancyManager set to limit scope of returned date IAW user authorization
- **api**: Adjust permissions for common viewset to use defaultdeny

### Fixes

- **access**: dont filter by id for tenant if no tenancies are defined
- **access**: Dont collect user tenancies for anon user
- **core**: use function get_tenant when fetching a models tenancy
- **api**: Return HTTP/500 if exception unknown
- **api**: add missing obj `_obj_tenancy` to common viewset

### Refactoring

- when fetching user settings, pk must be user_id
- **api**: Support url kwargs that uses attr sub_model_type
- **core**: rename ticket related serializers to use new way of doing business
- **api**: API exception always to convert to drf APIException
- **access**: move function `get_queryset` from tenancy mixin to common ViewSet
- **api**: Split Common ViewSet based off of permissions
- **access**: role queryset to use parent mthod for `get_queryset`
- **access**: Move manager to own dir
- **access**: migrate tenancy permissions to own ViewSetMixin
- **access**: refactor tenancy permission mixin
- **access**: move function get_parent_obj to common viewset
- **access**: move function get_permission_required to common viewset
- **access**: move function get_parent_model to common viewset
- **access**: get_tenancy function moved mixin organization -> permissions

### Tests

- **api**: Unit Test suite for DefaultDeny Permissions
- **access**: Unit Test suite for User Permissions
- **access**: Unit Test suite for SuperUser Permissions
- **access**: Add User Manager Unit Test Suite with test cases
- **access**: Tenancy Manager Unit Test cases for filtering and select_related
- **access**: Add tenancy Manager Unit Test Suite
- **access**: Add common Manager Unit Test Suite
- **settings**: Add Functional TestSuite for model AppSettings ViewSet
- **settings**: Add Functional TestSuite for model ExternalLinks ViewSet
- **itam**: Add Functional TestSuite for model SoftwareVersion ViewSet
- **itam**: Add Functional TestSuite for model SoftwareCategory ViewSet
- **settings**: Add Functional TestSuite for model UserSettings ViewSet
- **api**: Add Functional TestSuite for model AuthToken ViewSet
- **human_resources**: Add Functional TestSuite for model Employee ViewSet
- **access**: Add Functional TestSuite for model Tenant ViewSet
- **access**: Add Functional TestSuite for model Role ViewSet
- **access**: Add Functional TestSuite for model Person ViewSet
- **access**: Add Functional TestSuite for model Entity ViewSet
- **access**: Add Functional TestSuite for model Contact ViewSet
- **access**: Add Functional TestSuite for model Company ViewSet
- **project_management**: Add Functional TestSuite for model ProjectType ViewSet
- **project_management**: Add Functional TestSuite for model ProjectState ViewSet
- **project_management**: Add Functional TestSuite for model ProjectMilestone ViewSet
- **project_management**: Add Functional TestSuite for model Project ViewSet
- **itim**: Add Functional TestSuite for model Service ViewSet
- **itim**: Add Functional TestSuite for model Port ViewSet
- **itim**: Add Functional TestSuite for model ClusterType ViewSet
- **itim**: Add Functional TestSuite for model Cluster ViewSet
- **itam**: Add Functional TestSuite for model Software ViewSet
- **itam**: Add Functional TestSuite for model OperatingSystemVersion ViewSet
- **itam**: Add Functional TestSuite for model OperatingSystem ViewSet
- **itam**: Add Functional TestSuite for model DeviceType ViewSet
- **itam**: Add Functional TestSuite for model DeviceModel ViewSet
- **itam**: Add Functional TestSuite for model Device ViewSet
- **devops**: Add Functional TestSuite for model SoftwareEnabledFeatureFlag ViewSet
- **devops**: Add Functional TestSuite for model FeaturFlag ViewSet
- **core**: Add Functional TestSuite for model Manufacturer ViewSet
- **config_management**: Add Functional TestSuite for model ConfigGroupSoftware ViewSet
- **config_management**: Add Functional TestSuite for model ConfigGroup ViewSet
- **assistance**: Add Functional TestSuite for model KnowledgeBaseCategory ViewSet
- **api**: Ensure mocked request within Functional ViewSet test suite includes kwargs and data objects
- **assistance**: Functional Test suite for KnowledgeBase ViewSet
- **api**: Common Functional Test suite for Common ViewSet
- **access**: Test cases for permission function is_tenancy_model
- **access**: ensure queryset sets up Tenancy model manager with user data
- **project_management**: to check viewset queryset cached results, kwargs must be populated
- **api**: Common ViewSet test suites should not pass test not required. instead xfail
- **api**: Add missing `parent_model` type for class attribute check of `parent_model`
- **api**: make queryset cache result test cases truely dynamic
- **access**: Add initial Tenancy mixin Unit test suite

## 1.21.1 (2025-08-30)

### Fixes

- **base**: add trailing slant to admin url

## 1.21.0 (2025-08-29)

### feat

- **access**: remove feature flag 2025-00003
- **access**: Ensure for Centurion user that direct assignement of permissions are ignored
- **api**: Add logging to token authentication
- **core**: log failed audit history creation
- Models that have a User field to ensure it's protecteed
- **access**: extend rol model field name length 30 -> 50
- **core**: log ALL errors from audithistory
- **core**: Remove teams from Linked Model
- **access**: Remove teams form Tenancy page
- **admin**: Add roles and groups for webmaster
- **access**: Tsers and groups field migrations for model Role
- **access**: Add users and groups field to model Role
- **base**: Add Group model ViewSet
- **base**: Add Group model serializer

### Fixes

- **core**: Audit history to be sorted by created DESC
- **core**: when checking for context check the class not the model
- **access**: Correct tenancy model detection to Centurion Mixin
- **api**: Only return the authenticated users tokens
- **access**: remove org_team url from serializers
- **api**: ensure the correct key is used for context.logger

### Refactoring

- **access**: Corrections to Permission Unit model test suite
- **access**: Corrections to CenturionUser Auth methods
- model context for user moved keys user -> <_meta.model_name>
- setup logging so it always runs, inc for tests
- switch test suites to from model Team -> Group
- **access**: Migrations for team model cleanup
- **access**: remove Team ViewSet
- **access**: remove TeamUser ViewSet
- **access**: remove TeamUser Serializer
- **access**: remove Team Serializer
- **access**: remove model TeamNotes
- **access**: remove model TeamHistory
- **base**: rename function get_organization -> get_tenant
- **base**: enable casting models to int to rtn its id
- **core**: Use context manager for model context
- migrate serializers from TeamBaseSerializer -> GroupBaseSerializer
- Adjust fields Team -> Group
- api_request_permissions fixture updated to obtain permissions from roles
- **api**: Nav menu permissions moved to obtain from user object
- **access**: Migrate Centurion User to obtain permissions from roles
- dont root load user model
- remove v2 from user url basename
- remove v2 from url basename
- **access**: Remove old test suites no longer required model Role
- **access**: ViewSet Unit Test Suite re-written to Pytest for model Role
- **access**: Serializer Unit Test Suite re-written to Pytest for model Role
- **access**: API Fields render Functional Test Suite re-written to Pytest for model Role
- **access**: Model Functional Test Suite re-written to Pytest for model Role
- **access**: API Metadata Functional Test Suite re-written to Pytest for model Role

### Tests

- **access**: Unit model test suite for model CenturionUser
- **api**: Ensure that when cheking perms items returned contains an item from users org
- **access**: Remove all tests model TeamUser
- **access**: Remove all tests model Team

## 1.20.2 (2025-08-25)

### Fixes

- **access**: When creating an item and tenancy not required, cater for this within authorization
- **access**: Update old models for new permssion check methods

### Tests

- **api**: Test case to confirm MetaData can be fetch for list action

## 1.20.1 (2025-08-22)

### Fixes

- **access**: Check both permissions and permissions by tenancy seperatly
- **access**: Ensure superuser check is done

## 1.20.0 (2025-08-22)

### feat

- **access**: Switch Tenancy Object to use refactord Tenancy Manager
- Switch authorization object from request.tenancy -> request.user
- **base**: Switch user model to CenturionUser
- **access**: CenturionUser model migrations

### Fixes

- **access**: When checking for user within TenancyManager, ensure it has an id
- **settings**: AppSettings model should return `owner_organization` for `get_organization`
- **access**: CenturionUser model must inherit from Abstract User
- dont load user object during app load

### Refactoring

- **access**: do prefetch user orgs, permissions and content_types
- **access**: rename mixin OrganizationPermissionMixin -> TenancyPermissionMixin
- **api**: ensure kwargs are copied for api perm test cases
- **core**: when deleting a model dont re-fetch from db, use current data

### Tests

- **functional**: Add Token Authentication Functional Test Suite
- **integration**: Test to ensure that migrations run successfully
- **access**: Correct TenantModelNote userOrgs fetch test case to use correct model
- **access**: Updated Test Suite for mixin TenancyPermission

## 1.19.3 (2025-08-17)

### Fixes

- **api**: ensure human_resources is behind its feature flag
- **human_resources**: correct index route name
- **access**: correct access route name

## 1.19.2 (2025-08-16)

### Fixes

- **base**: before setting up metrics if enabled, create data dir

## 1.19.1 (2025-08-15)

### Fixes

- **docker**: if not testing dont attempt to import coverage

## 1.19.0 (2025-08-15)

### feat

- **core**: add to migration signal system user and use for inventory objects
- **docker**: Adjust gunicorn works=4 100reqs/max and preload app
- **api**: Ensure that serializer converts Django exceptions to rest_framework exceptions
- **access**: Filter history permissions
- **access**: Add Audit and notes tables for model Role
- **access**: Add AuditHistory Serializer for Role model
- **access**: Add Notes Serializer for Role model
- **itam**: Add AuditHistory Serializer for ITAMAssetBase model
- **itam**: Add Notes Serializer for ITAMAssetBase model
- **accounting**: Add AuditHistory Serializer for AssetBase model
- **accounting**: Add Notes Serializer for AssetBase model
- When attempting to create and objetc must be unique and alrready exists, dont return error return existing object
- **access**: History + Notes model migrations for Company Model
- **api**: map notfound and perm denied django -> drf exceptions
- **human_resources**: Add model tag for Employee model
- **human_resources**: Add AuditHistory Serializer for Employee model
- **human_resources**: Add Notes Serializer for Employee model
- **human_resources**: Change model to inherit from `CenturionModel` for Employee model
- **access**: Add model tag for Person model
- **access**: Add AuditHistory Serializer for Person model
- **access**: Add Notes Serializer for Person model
- **access**: Change model to inherit from `CenturionModel` for Person model
- **access**: Add model tag for Contact model
- **access**: Add AuditHistory Serializer for Contact model
- **access**: Add Notes Serializer for Contact model
- **access**: Change model to inherit from `CenturionModel` for Contact model
- **access**: Add AuditHistory Serializer for Company model
- **access**: Add Notes Serializer for Entity model
- **access**: Change model to inherit from `CenturionModel` for Company model
- **access**: Change model to inherit from `CenturionModel` for Entity model
- **access**: Add AuditHistory Serializer for Entity model
- **access**: Add Notes Serializer for Entity model
- **access**: Change model to inherit from `CenturionModel` for Entity model
- **settings**: Add model tag for ExtrnalLink model
- **settings**: Add AuditHistory Serializer for UserSettings model
- **settings**: Add Notes Serializer for UserSettings model
- **settings**: Change model to inherit from `CenturionModel` for UserSettings model
- **settings**: Add model ExternalLink to migrate for history and notes
- **settings**: Add AuditHistory Serializer for ExternalLink model
- **settings**: Add Notes Serializer for ExternalLink model
- **settings**: Change model to inherit from `CenturionModel` for ExternalSettings model
- **settings**: Add model AppSettings to migrate for history and notes
- **settings**: Add AuditHistory Serializer for AppSettings model
- **settings**: Add Notes Serializer for AppSettings model
- **settings**: Change model to inherit from `CenturionModel` for AppSettings model
- **project_management**: Add model ProjectType to migrate for history and notes
- **project_management**: Add AuditHistory Serializer for ProjectTYpe model
- **project_management**: Add Notes Serializer for ProjectType model
- **project_management**: Change model to inherit from `CenturionModel` for ProjectType model
- **project_management**: Add model ProjectState to migrate for history and notes
- **project_management**: Add AuditHistory Serializer for ProjectState model
- **project_management**: Add Notes Serializer for ProjectState model
- **project_management**: Change model to inherit from `CenturionModel` for ProjectState model
- **project_management**: Add model ProjectMilestone to migrate for history and notes
- **project_management**: Add AuditHistory Serializer for ProjectMilestone model
- **project_management**: Add Notes Serializer for ProjectMilestone model
- **project_management**: Change model to inherit from `CenturionModel` for ProjectManagement model
- **project_management**: Add model Project to migrate for history and notes
- **project_management**: Add AuditHistory Serializer for Project model
- **project_management**: Add Notes Serializer for Project model
- **project_management**: Change model to inherit from `CenturionModel` for Project model
- **itim**: Add model Service to migrate for history and notes
- **itim**: Add AuditHistory Serializer for Service model
- **itim**: Add Notes Serializer for Service model
- **itim**: Change model to inherit from `CenturionModel` for Service model
- **itim**: Add model Port to migrate for history and notes
- **itim**: Add AuditHistory Serializer for Port model
- **itim**: Add Notes Serializer for Port model
- **itim**: Change model to inherit from `CenturionModel` for Port model
- **itim**: Add AuditHistory Serializer for ClusterType model
- **itim**: Add Notes Serializer for ClusterType model
- **itim**: Change model to inherit from `CenturionModel` for ClusterType model
- **itim**: Add model Cluster to migrate for history and notes
- **itim**: Add Notes Serializer for Cluster model
- **itim**: Add AuditHistory Serializer for Cluster model
- **itim**: Change model to inherit from `CenturionModel` for Cluster model
- **itam**: Add model SoftwareVersion to migrate for history and notes
- **itam**: Add Notes Serializer for SoftwareVersiony model
- **itam**: Add AuditHistory Serializer for SoftwareVersion model
- **itam**: Change model to inherit from `CenturionModel` for SoftwareVersion model
- **itam**: Add model SoftwareCategory to migrate for history and notes
- **itam**: Add Notes Serializer for SoftwareCategory model
- **itam**: Add AuditHistory Serializer for SoftwareCategory model
- **itam**: Change model to inherit from `CenturionModel` for SoftwareCategory model
- **itam**: Add model Software to migrate for history and notes
- **itam**: Add Notes Serializer for Software model
- **itam**: Add AuditHistory Serializer for Software model
- **itam**: Change model to inherit from `CenturionModel` for Software model
- **itam**: Add model OperatingSystemVersion to migrate for history and notes
- **itam**: Add Notes Serializer for OperatingSystemVersion model
- **itam**: Add AuditHistory Serializer for OperatingSystemVersion model
- **itam**: Change model to inherit from `CenturionModel` for OperatingSystemVersion model
- **itam**: Add model OperatingSystem to migrate for history and notes
- **itam**: Add Note Serializer for DeviceSoftware model
- **itam**: Add AuditHistory Serializer for DeviceSoftware model
- **itam**: Change model to inherit from `CenturionModel` for DeviceSoftware model
- **itam**: Change model to inherit from `Centurion` for DeviceSoftware model
- **itam**: Add model_tag to DeviceType model
- **itam**: Add DeviceType for history and notes data migration
- **itam**: Add DeviceModel for history and notes data migration
- **itam**: Add DEvice for history and notes data migration
- **devops**: Switch SoftwareEnabledFeatureFlag model to inherit from CenturionModel
- **devops**: Update checkin model fixture so it creates the feature flag
- **devops**: Add methods get_url and get_url_kwargs to CheckIn model
- **devops**: Add migration to signal
- **devops**: Add migration to signal
- **devops**: Add migration to signal
- **devops**: Add migration to signal
- **devops**: Update URL route basename
- **devops**: Migrations for switching GitLabRepository model to inherit from `CenturionModel`
- **devops**: Migrations for switching GitRepository model to inherit from `CenturionModel`
- **devops**: Migrations for switching GitRepository model to inherit from `CenturionModel`
- **devops**: Serializers for GitRepository models notes and history
- **devops**: Serializers for GitHubGitRepository models notes and history
- **devops**: Serializers for GitLabGitRepository models notes and history
- **devops**: Switch GitLabGitRepository model to inherit from `CenturionModel`
- **devops**: Switch GitHubGitRepository model to inherit from `CenturionModel`
- **devops**: Switch GitRepository model to inherit from `CenturionModel`
- **devops**: Update Checkin model url route basename
- **devops**: Add app_namespace Checkin model
- **devops**: Add Checkin to migrate model history/notes
- **devops**: Migrations for switching Checkin model to inherit from `CenturionModel`
- **devops**: Switch Checkin model to inherit from `CenturionModel`
- **core**: add TicketCommentCategory to history/notes migration
- **core**: add model tag to ticket comment category
- **core**: Migrations for TicketCategory
- **core**: add TicketCategory to history/notes migration
- **core**: add model tag to ticket category
- **core**: add Manufacturer to history/notes migration
- **core**: add model tag to manufacturer
- **config_management**: add ConfigGroups to history/notes migration
- **config_management**: add ConfigGroupSoftware to history/notes migration
- **config_management**: add ConfigGroupHosts to history/notes migration
- **access**: add tenant to history/notes migration
- **access**: Migration for switching model inheritence to `CenturionModel`
- **itam**: Update model methods
- **access**: Migration for switching model inheritence to `CenturionMixin`
- **access**: Switch model inheritence to `CenturionMixin`
- **itam**: Update url basename
- **itam**: Update url basename
- **base**: add support for manytomany for model unit tests
- **itam**: Update url basename
- **core**: Update url basename
- **core**: Update url basename
- **core**: Update url basename
- **core**: Update url basename
- **core**: Update url basename
- **core**: Update url basename
- **access**: TeamUsers do not require notes
- **config_management**: ConfigGroupHosts and ConfigGroupSoftware do not require notes
- **config_management**: Add url_kwargs to ConfigGroupSoftware model
- **access**: Add url_kwargs to Team model
- **access**: Add url_kwargs to TeamUser model
- **access**: Update TeamUser API basename
- **access**: Update Team API basename
- **itam**: switch model Device to inheirt from CenturionModel
- **itam**: switch model DeviceType to inheirt from CenturionModel
- **itam**: switch model DeviceModel to inheirt from CenturionModel
- **core**: switch model TicketCategory to inheirt from CenturionModel
- **core**: switch model TicktetCommentCategory to inheirt from CenturionModel
- **core**: switch model Manufacturer to inheirt from CenturionModel
- **config_management**: switch model ConfigGroupHosts to inheirt from CenturionModel
- **config_management**: switch model ConfigGroupSoftware to inheirt from CenturionModel
- **config_management**: switch model ConfigGroups to inheirt from CenturionModel
- **access**: switch model TeamUsers to inheirt from CenturionModel
- **access**: switch model Team to inheirt from CenturionModel
- **core**: If user context not supplied, dont create audithistory for model
- **access**: Add init to tenancy model to clear state
- **core**: Ensure that model has user context
- **core**: Add supprt to model_instance fixture for manytomany field
- **core**: Add supprt to model create test for manytomany field
- **assistance**: migrations for new history and notes models for KnowledgeBaseCategory model
- **assistance**: migrations for new history and notes models for KnowledgeBase model
- **assistance**: Model inheritance migrations
- **core**: Migrate Centurion Model history and notes within a post_migrate signal
- **core**: Add ability to CenturionModel `get_url` to be either detail/list
- **core**: New Management command to list models
- **devops**: Switch model FeatureFlag inheritance to CenturionModel
- **core**: Disable Notes for model CenturionModelNote
- **devops**: Enable Model notes for GitGroup
- **core**: add Swagger docs for CenturionModelNotes ViewSet
- **core**: Meta Model for CenturionModelNotes
- **core**: Finalize Serializer for CenturionModelNotes
- **api**: Add to common serializer meta notes model for notes url
- **core**: Interim Meta model CenturionNotes
- **core**: Interim ViewSet for model CenturionNotes
- **core**: URL Route for model CenturionNotes
- **core**: Serializer for model CenturionNotes
- **core**: Migration for model CenturionNotes
- **core**: Add model CenturionNotes
- **devops**: dont allow deleting a git group if it has children
- **devops**: Add model tag attribute to model
- **core**: Add to Centurion Model an attribute to set the models tag
- **core**: Add Context to model when ViewSet loads
- **devops**: Add AuditHistory Serializer for GitGroup
- **core**: Add AuditHistory Serializer
- **core**: Add AuditHistory ViewSet
- **core**: Add URL route for AuditHistory
- **core**: Add audithistory URL to serializer for models with `_audit_enabled=True`
- **core**: Models url kwarg helper
- **core**: Support setting custom model name for url basename
- **api**: Add sub-model filter to `get_queryset` method
- **core**: Disable models audit history on model delete
- **core**: Use Previous TenancyManager until UserModel rewrite done
- **core**: Process a models history within AuditHistory
- **core**: Enable AuditHistory signal to start when apps are ready
- **core**: Add model instance to history object during history creation
- **core**: Update Meta AuditModel `db_name` to be suffixed `_audithistory`
- **core**: remove unnessecary method `clean_fields` from audit model
- **core**: remove un-needed field `model_notes` from audit models
- **core**: Run meta models create on Core module ready
- **core**: New model core.CenturionAudit
- **core**: cause sub-audit models to chuck a wobbler if clean_fields not re-implementated
- **access**: remove mill-seconds from datetime auto fields
- **core**: Centurion model Base
- **core**: Centurion Audit model
- **core**: permissions getter for role model
- **core**: Audit History Signal for Delete/Save
- **core**: Dynamic History model creation

### Fixes

- remove trailing slant from URLs
- **access**: When creating permission QuerySet prevent app crash if db not setup
- **itim**: Ensure during testing, fixture vals are copied for Model Service
- **base**: on fixture cleanup, only clean if obj exists
- **core**: required field must be null for logical chek to function
- **itam**: field slug no longer avail, use str
- **core**: Include model so content type is created
- **settings**: AppSettings requires super user perms
- **api**: Convert Django Exceptions to DRF API Exception equivilent
- **api**: Ensure if exception DRF, message returned is from that exception
- **devops**: git repository is sub-model ViewSet must inherit from SubModel
- **access**: entity field `entity_type` is an auto field
- **access**: Ensure that if method not allowed, exception is thrown first before perms check
- **itam**: Model software must be related linked to organization model
- **access**: if user has no orgs, dont filter by for query
- **devops**: Ensure mandatory fields are writeable for model GitRepository
- **access**: add property organization to Tenant model
- **itam**: Add missing import `now`
- **core**: notes meta model must add `model_kwargs` fixture
- **core**: clean_fields for created_by field belongs in model that contains field
- **core**: audit meta model must add `model_kwargs` fixture
- model fixture names must match model_name
- clean up mock model from django apps
- **core**: When obtaining model fields ensure it exists first
- **access**: use getattr instead as attribute may exist as None
- **assistance**: make kb article field longer for model name
- **assistance**: Add missing field `model_notes` to KB serializer
- **core**: Before attempting to get model audit data confirm fields dont already exist
- **api**: check if model has notes enabled before adding url to body
- **api**: Only return View Serialized data if status code is HTTP/2xx
- **core**: Conduct kwargs check fr ticket comment serializer during init
- **core**: Enable CenturionAudit model to get model history for item being deleted
- **core**: When creating the AuditHistory entry for a model, use the user from context
- **core**: When collecting AuditHistory cater for models being created
- **api**: remove surerflous feature for fetching app_namespace for models metadata
- **core**: Correct attribute names for referencing a Centurion Model from an AuditModel
- **core**: Correct before lookup for current models audit history
- **core**: When deleting a model check if sub-model within delete method
- **access**: Tenancy Manager should not attempt to get org as related field if it does not exist
- **api**: ensure val returns at least none

### Refactoring

- **docker**: update healthcheck interval=10s and start-period=30s
- **docker**: when l;aunching gunicorn create a pid file
- **devops**: API Fields render Functional Test Suite re-written to Pytest for model SoftwareEnableFeatureFlag Again
- **devops**: Remove old test suites no longer required model SoftwareEnableFeatureFlag
- **devops**: ViewSet Unit Test Suite re-written to Pytest for model SoftwareEnableFeatureFlag
- **devops**: Serializer Unit Test Suite re-written to Pytest for model SoftwareEnableFeatureFlag
- **devops**: API Fields render Functional Test Suite re-written to Pytest for model SoftwareEnableFeatureFlag
- **devops**: Model Functional Test Suite re-written to Pytest for model SoftwareEnableFeatureFlag
- **devops**: API Metadata Functional Test Suite re-written to Pytest for model SoftwareEnableFeatureFlag
- **devops**: Remove old test suites no longer required model FeatureFlag
- **devops**: ViewSet Unit Test Suite re-written to Pytest for model FeatureFlag
- **devops**: Serializer Unit Test Suite re-written to Pytest for model FeatureFlag
- **devops**: API Fields render Functional Test Suite re-written to Pytest for model FeatureFlag
- **devops**: Model Functional Test Suite re-written to Pytest for model FeatureFlag
- **devops**: API Metadata Functional Test Suite re-written to Pytest for model FeatureFlag
- **api**: Remove old test suites no longer required model AuthToken
- **api**: ViewSet Unit Test Suite re-written to Pytest for model AuthToken
- **api**: Serializer Unit Test Suite re-written to Pytest for model AuthToken
- **api**: API Fields render Functional Test Suite re-written to Pytest for model AuthToken
- **api**: Model Functional Test Suite re-written to Pytest for model AuthToken
- **api**: API Metadata Functional Test Suite re-written to Pytest for model AuthToken
- **access**: Remove old test suites no longer required model Tenant
- **access**: Serializer Unit Test Suite re-written to Pytest for model Tenant
- **access**: API Fields render Functional Test Suite re-written to Pytest for model Tenant
- **access**: Model Functional Test Suite re-written to Pytest for model Tenant
- **access**: API Metadata Functional Test Suite re-written to Pytest for model Tenant
- **settings**: Remove old test suites no longer required model UserSettings
- **settings**: ViewSet Unit Test Suite re-written to Pytest for model UserSettings
- **settings**: Serializer Unit Test Suite re-written to Pytest for model UserSettings
- **settings**: API Fields render Functional Test Suite re-written to Pytest for model UserSettings
- **settings**: Model Functional Test Suite re-written to Pytest for model UserSettings
- **settings**: API Metadata Functional Test Suite re-written to Pytest for model UserSettings
- **settings**: Remove old test suites no longer required model ExternalLink
- **settings**: ViewSet Unit Test Suite re-written to Pytest for model ExternalLink
- **settings**: Serializer Unit Test Suite re-written to Pytest for model ExternalLink
- **settings**: API Fields render Functional Test Suite re-written to Pytest for model ExternalLink
- **settings**: Model Functional Test Suite re-written to Pytest for model ExternalLink
- **settings**: API Metadata Functional Test Suite re-written to Pytest for model ExternalLink
- **settings**: Remove old test suites no longer required model AppSettings
- **settings**: ViewSet Unit Test Suite re-written to Pytest for model AppSettings
- **settings**: Serializer Unit Test Suite re-written to Pytest for model AppSettings
- **settings**: API Fields render Functional Test Suite re-written to Pytest for model AppSettings
- **settings**: Model Functional Test Suite re-written to Pytest for model AppSettings
- **settings**: API Metadata Functional Test Suite re-written to Pytest for model AppSettings
- **test**: remove xfail during `pytest_generate_tests` before parameterizing
- **project_management**: ensure within fixtur kwargs are copied
- **project_management**: Remove old test suites no longer required model ProjectType
- **project_management**: ViewSet Unit Test Suite re-written to Pytest for model ProjectType
- **project_management**: Serializer Unit Test Suite re-written to Pytest for model ProjectType
- **project_management**: API Fields render Functional Test Suite re-written to Pytest for model ProjectType
- **project_management**: Model Functional Test Suite re-written to Pytest for model ProjectType
- **project_management**: API Metadata Functional Test Suite re-written to Pytest for model ProjectType
- **project_management**: Remove old test suites no longer required model ProjectState
- **project_management**: ViewSet Unit Test Suite re-written to Pytest for model ProjectState
- **project_management**: Serializer Unit Test Suite re-written to Pytest for model ProjectState
- **project_management**: API Fields render Functional Test Suite re-written to Pytest for model ProjectState
- **project_management**: Model Functional Test Suite re-written to Pytest for model ProjectState
- **project_management**: API Metadata Functional Test Suite re-written to Pytest for model ProjectState
- **project_management**: Remove old test suites no longer required model ProjectMilestone
- **project_management**: ViewSet Unit Test Suite re-written to Pytest for model ProjectMilestone
- **project_management**: Serializer Unit Test Suite re-written to Pytest for model ProjectMilestone
- **project_management**: API Fields render Functional Test Suite re-written to Pytest for model ProjectMilestone
- **project_management**: Model Functional Test Suite re-written to Pytest for model ProjectMilestone
- **project_management**: API Metadata Functional Test Suite re-written to Pytest for model ProjectMilestone
- **project_management**: Remove old test suites no longer required model Project
- **project_management**: ViewSet Unit Test Suite re-written to Pytest for model Project
- **project_management**: Serializer Unit Test Suite re-written to Pytest for model Project
- **project_management**: API Fields render Functional Test Suite re-written to Pytest for model Project
- **project_management**: Model Functional Test Suite re-written to Pytest for model Project
- **project_management**: API Metadata Functional Test Suite re-written to Pytest for model Project
- **itim**: Remove old test suites no longer required model Service
- **itim**: ViewSet Unit Test Suite re-written to Pytest for model Service
- **itim**: Serializer Unit Test Suite re-written to Pytest for model Service
- **itim**: API Fields render Functional Test Suite re-written to Pytest for model Service
- **itim**: Model Functional Test Suite re-written to Pytest for model Service
- **itim**: API Metadata Functional Test Suite re-written to Pytest for model Service
- **itim**: Remove old test suites no longer required model Port
- **itim**: ViewSet Unit Test Suite re-written to Pytest for model Port
- **itim**: Serializer Unit Test Suite re-written to Pytest for model Port
- **itim**: API Fields render Functional Test Suite re-written to Pytest for model Port
- **itim**: Model Functional Test Suite re-written to Pytest for model Port
- **itim**: API Metadata Functional Test Suite re-written to Pytest for model Port
- **itim**: Remove old test suites no longer required model ClusterType
- **itim**: ViewSet Unit Test Suite re-written to Pytest for model ClusterType
- **itim**: Serializer Unit Test Suite re-written to Pytest for model ClusterType
- **itim**: API Fields render Functional Test Suite re-written to Pytest for model ClusterType
- **itim**: Model Functional Test Suite re-written to Pytest for model ClusterType
- **itim**: API Metadata Functional Test Suite re-written to Pytest for model ClusterType
- **itim**: Remove old test suites no longer required model Cluster
- **itim**: ViewSet Unit Test Suite re-written to Pytest for model Cluster
- **itim**: Serializer Unit Test Suite re-written to Pytest for model Cluster
- **itim**: API Fields render Functional Test Suite re-written to Pytest for model Cluster
- **itim**: Model Functional Test Suite re-written to Pytest for model Cluster
- **itim**: API Metadata Functional Test Suite re-written to Pytest for model Cluster
- **itam**: Remove old test suites no longer required model SoftwareVersion
- **itam**: ViewSet Unit Test Suite re-written to Pytest for model SoftwareVersion
- **itam**: Serializer Unit Test Suite re-written to Pytest for model SoftwareVersion
- **itam**: Model Functional Test Suite re-written to Pytest for model SoftwareVersion
- **itam**: API Fields render Functional Test Suite re-written to Pytest for model SoftwareVersion
- **itam**: API Metadata Functional Test Suite re-written to Pytest for model SoftwareVersion
- **itam**: Remove old test suites no longer required model SoftwareCategory
- **itam**: ViewSet Unit Test Suite re-written to Pytest for model SoftwareCategory
- **itam**: Serializer Unit Test Suite re-written to Pytest for model SoftwareCategory
- **itam**: Model Functional Test Suite re-written to Pytest for model SoftwareCategory
- **itam**: API Fields render Functional Test Suite re-written to Pytest for model SoftwareCategory
- **itam**: API Metadata Functional Test Suite re-written to Pytest for model SoftwareCategory
- **itam**: Remove old test suites no longer required model Software
- **itam**: ViewSet Unit Test Suite re-written to Pytest for model Software
- **itam**: Serializer Unit Test Suite re-written to Pytest for model Software
- **itam**: Model Functional Test Suite re-written to Pytest for model Software
- **itam**: API Fields render Functional Test Suite re-written to Pytest for model Software
- **itam**: API Metadata Functional Test Suite re-written to Pytest for model Software
- **itam**: Remove old test suites no longer required model OperatingSystemVersion
- **itam**: ViewSet Unit Test Suite re-written to Pytest for model OperatingSystemVersion
- **itam**: Serializer Unit Test Suite re-written to Pytest for model OperatingSystemVersion
- **itam**: Model Functional Test Suite re-written to Pytest for model OperatingSystemVersion
- **itam**: API Fields render Functional Test Suite re-written to Pytest for model OperatingSystemVersion
- **itam**: API Metadata Functional Test Suite re-written to Pytest for model OperatingSystemVersion
- **itam**: Remove old test suites no longer required model OperatingSystem
- **itam**: ViewSet Unit Test Suite re-written to Pytest for model OperatingSystem
- **itam**: Serializer Unit Test Suite re-written to Pytest for model OperatingSystem
- **itam**: Model Functional Test Suite re-written to Pytest for model OperatingSystem
- **itam**: API Fields render Functional Test Suite re-written to Pytest for model OperatingSystem
- **itam**: API Metadata Functional Test Suite re-written to Pytest for model OperatingSystem
- **itam**: API Metadata Functional Test Suite re-written to Pytest for model DeviceType
- **itam**: Model Functional Test Suite re-written to Pytest for model DeviceType
- **itam**: API Fields render Test Suite re-written to Pytest for model DeviceType
- **itam**: Serializer Unit Test Suite re-written to Pytest for model DeviceType
- **itam**: ViewSet Unit Test Suite re-written to Pytest for model DeviceModel
- **itam**: API Metadata Functional Test Suite re-written to Pytest for model DeviceModel
- **itam**: API Field Render Functional Test Suite re-written to PyTest for model Device
- **itam**: Metadate Functional Test Suite re-enabled for model Device
- **itam**: Viewset Unit Test Suite re-written to pytest for model Device
- **itam**: Serializer Unit Test Suite re-enabled for model Device
- **core**: API Render Unit Test Suite re-enabled for model Manufacturer
- **core**: API Metadata Functional Test Suite re-enabled for model Manufacturer
- **core**: Serializer Functional Test Suite re-enabled for model Manufacturer
- **core**: ViewSet Test Suite re-written to pytest for model Manufacturer
- **config_management**: ViewSet Test Suite re-written to pytest for model ConfigGroupSoftware
- **config_management**: API fields Test Suite  re-enalbed for model ConfigGroupSoftware
- **config_management**: API Metadata Functional Test Suite for model ConfigGroupSoftware
- **config_management**: Serializer Functional Test Suite Enabled for model ConfigGroupSoftware
- **config_management**: Model Unit Test Suite re-written to pytest for model ConfigGroup
- **config_management**: API Metadata Functional Test Suite re-written to pytest for model ConfigGroup
- **assistance**: Serializer Unit Test Suite re-written to pytest for model KnowledgeBase
- **assistance**: MetaData Unit Test Suite re-written to pytest for model KnowledgeBaseCategory
- **assistance**: Serializer Unit Test Suite re-written to pytest for model KnowledgeBaseCategory
- **assistance**: ViewSet Unit Test Suite re-written to pytest for model KnowledgeBaseCategory
- **assistance**: Serializer Unit Test Suite re-written to pytest for model KnowledgeBaseCategory
- **assistance**: Serializer Unit TestSuite re-written to pytest for model KnowledgeBase
- **assistance**: ViewSet TestSuite re-written to pytest for model KnowledgeBase
- **access**: ViewSet TestSuite re-written to pytest for model Tenant
- **access**: ViewSet TestSuite re-written to pytest for model Person
- **access**: ViewSet TestSuite re-written to pytest for model Entity
- **access**: ViewSet TestSuite re-written to pytest for model Contact
- **access**: ViewSet TestSuite re-written to pytest for model Company
- **api**: migrate Common ViewSet unittest.mock to mocker
- **api**: migrate Common ViewSet Unit Test Suite attribute to use test case `unit_class`
- **api**: Converted Common ViewSet Unit Test Suite to use Pytest
- **api**: partial conversion to pytest for Common ViewSet Unit Test Suite
- **api**: Rename create Serializer unit test to `is_valid`
- **base**: normalize empty/not used to be `models.NOT_PROVIDED`
- **base**: adjust functional model test to use fixture kwargs
- **api**: Update Test Suite for AuthToken model
- **tests**: Unskip tests that'll work now due to model inheritance change
- **api**: Update Test Suite for AuthToken model
- **api**: Update URL route name for Role AuthToken
- **api**: Switch to inherit from Centurion model for model AuthToken
- **access**: When adding model role via api, status is 201/created
- **itim**: Update Test Suite for TicketCommentSolution model
- **itim**: Update Test Suite for TicketSLM model
- **itim**: Update Test Suite for TicketRequest model
- **core**: Update Test Suite for TicketBase model
- **core**: Update Test Suite for TicketCommentSolution model
- **core**: Update Test Suite for TicketCommentAction model
- **core**: Update Test Suite for TicketCommentBase model
- **core**: Initial Update Test Suite for TicketCommentBase model
- **core**: Update Tests to cater for inheritence changes
- **itim**: Update Test Suite for RequestTicket model
- **itim**: Update Test Suite for SLMTicket model
- **itim**: Update Test Suite for SLMTicket model
- **core**: Update Test Suite for TicketBase model
- **core**: Update Test Suite for TicketBase model
- **core**: Switch to inherit from Centurion model for model TicketBase
- **core**: Switch to inherit from Centurion model for model SLMTicketBase
- **core**: Update URL route name for Role TicketCommentBase
- **core**: Switch to inherit from Centurion model for model TicketCommentBase
- **core**: Update URL route name for Role TicketBase
- **core**: Switch to inherit from Centurion model for model TicketBase
- **core**: Add fn get_organization to centurion mixin
- **access**: Adjust add permission test for model Role
- **access**: Migrations for Inheritance change for Role model
- **access**: Update URL route name for Role model
- **access**: Update Test Suite for Role model
- **access**: Switch to inherit from Centurion model for model Role
- Asset and ITAM Asset must use url kwarg model_name not asset_model
- **accounting**: Update existing tests to work due to  model inheritance changes
- **itam**: Update URL route name for ITAMAssetBase model
- **itam**: Update Test Suite for ITAMAssetBase model
- **itam**: Switch to inherit from Centurion model for model ITAMAssetBase
- **accounting**: Switch to inherit from Centurion model for model AssetBase
- **accounting**: Update URL route name for AssetBase model
- **accounting**: Update Test Suite for AssetBase model
- **accounting**: Switch to inherit from Centurion model for model AssetBase
- **api**: dont query db for instance, use existing from response
- **api**: additional perms tests if they exist must be inc first
- **devops**: remove ViewSet `get_queryset` function
- **access**: Update Entity model ViewSet attribute `model_kwarg` to `model_name`
- **access**: Update Entity model ViewSet to inherit from submodel-rewrite
- **access**: Update Test Suite for Employee model
- **access**: Update Test Suite for Person model
- **access**: Update Test Suite for Contact model
- **access**: Update Test Suite for Company model
- **access**: Update URL route name for Entity model
- **access**: Update Test Suite for Entity model
- **access**: Update is_tenancy_object to check for CenturionModel
- **access**: For request middleware, use filter and first object so that testing can occur when mre than one exists
- **settings**: Update URL route name for UserSettings model
- **settings**: Update Test Suite for ExternalLink model
- **settings**: Update URL route name for ExternalLink model
- **settings**: Update Test Suite for ExternalLink model
- **settings**: Update URL route name for AppSettings model
- **settings**: Update Test Suite for AppSettings model
- **project_management**: Update URL route name for ProjectType model
- **project_management**: Update Test Suite for ProjectType model
- **project_management**: Update URL route name for ProjectState model
- **project_management**: Update Test Suite for ProjectState model
- **project_management**: Update URL route name for ProjectMilestone model
- **project_management**: Update Test Suite for ProjectMilestone model
- **project_management**: Update URL route name for Project model
- **project_management**: Update Test Suite for Project model
- **itim**: Update URL route name for Service model
- **itim**: Update Test Suite for Service model
- **itim**: Update URL route name for Port model
- **itim**: Update Test Suite for Port model
- **itim**: Update URL route name for ClusterType model
- **itim**: Update Test Suite for ClusterType model
- **itim**: Update URL route name for Cluster model
- **itim**: Update Test Suite for Cluster model
- **itam**: Update Test Suite for SoftwareVersion model
- **itam**: Update URL route name for SoftwareVersion model
- **itam**: Update Test Suite for SoftwareCategory model
- **itam**: Update URL route name for SoftwareCategory model
- cater for dev that does not exist in test cleanup
- **itam**: Update Test Suite for Software model
- **itam**: Update URL route name for Software model
- **itam**: Update Test Suite for OperatingSystemVersion model
- **itam**: Update Test Suite for OperatingSystem model
- **itam**: Update URL route name for DeviceSoftware model
- **itam**: Update Test Suite for DeviceSoftware model
- **itam**: Update Test Suite for DeviceDeviceOperatingSystem model
- **itam**: Update URL route for DeviceDeviceOperatingSystem model
- **itam**: Migration for updating model inheritance for DeviceDeviceOperatingSystem model
- **itam**: Updated Unit model test suite for DeviceType model
- **devops**: Updated Unit model test suite for DeviceModel model
- **devops**: Migration for updating model inheritance for DeviceModel model
- **itam**: Updated Unit model test suite for Device model
- **devops**: Updated Unit model test ssuite for SoftwareEnabledFeatureFlag model
- **devops**: Migration for updating model inheritance for SoftwareEnabledFeatureFlag model
- **devops**: Update url route basename for SoftwareEnabledFeatureFlag model
- **tests**: make all `parameterized_` vars properties
- **core**: adjust CenturionSubModel to not be it's own inheritable class
- **core**: Move CenturionModel logic to Mixin
- **core**: rename mixin -> mixins
- **base**: model instancxe code de-duplicated
- **config_management**: Add ConfigGroupHost Model Tests
- **config_management**: Add ConfigGroupSoftware Model Tests
- **config_management**: Add ConfigGroup Model Tests
- **assistance**: Refactor KnowledgeBaseCategory Unit model tests
- **assistance**: Update KnowledgeBase Unit viewset url basename
- **assistance**: Refactor KnowledgeBase Unit model tests
- **assistance**: Add new history and notes Serializer for KnowledgeBase model
- **assistance**: Add new history and notes Serializer for KnowledgeBaseCategory model
- **assistance**: Change KnowledgeBaseCategory model inheritance TenancyObject -> CenturionModel
- **assistance**: Change KnowledgeBase model inheritance TenancyObject -> CenturionModel
- **assistance**: MV kb category model to its own file
- **tests**: Create global model fixtures
- **devops**: Switch FeatureFlag model unit  tests to CenturionModel
- **settings**: move url routes from core.urls to own module `urls_api.py`
- **project_management**: move url routes from core.urls to own module `urls_api.py`
- **itim**: move url routes from core.urls to own module `urls_api.py`
- **itam**: move url routes from core.urls to own module `urls_api.py`
- **core**: move url routes from core.urls to own module `urls_api.py`
- **config_management**: move url routes from core.urls to own module `urls_api.py`
- **assistance**: move url routes from core.urls to own module `urls_api.py`
- **access**: move url routes from core.urls to own module `urls_api.py`
- **api**: Update Common ViewSet methds for re-write
- **devops**: Switch GitGroup Model to CenturionModel
- **core**: Loading of meta models should not be hidden behind program start ags
- **core**: To obtain audit_values loop through model fields
- rejig whats in each inherited centurion model
- **access**: prefetch org with tenancy object
- **core**: Relocate history model class
- **base**: rename app to centurion

### Tests

- **core**: Notes Meta Models API Permissions Test cases for All Notes Models
- Add initial integration tests
- **docker**: Add compose setup for  integration testing
- **itam**: ViewSet Unit Test Suite added for model DeviceType
- **itam**: Serializer UnitTest Suite added for model DeviceModel
- **itam**: API Fields render Functional Test Suite added for model DeviceModel
- **itam**: Model Functional Test Suite added for model DeviceModel
- **itam**: Refactor failing tests to cater for uniqueness so they pass
- **itam**: Model Functional Test Suite aded for model Device
- **config_management**: ViewSet Unit Test Suite re-written to pytest for model ConfigGroup
- **config_management**: Serializer Unit Test Suite re-written to pytest for model ConfigGroup
- **config_management**: Model Functional Test Suite re-written to pytest for model ConfigGroup
- **config_management**: API Field Render Functional Test Suite re-written to pytest for model ConfigGroup
- **assistance**: API Field Render Functional Test Suite re-written to pytest for model KnowledgeBaseCategory
- **assistance**: Model Functional Test Suite re-written to pytest for model KnowledgeBaseCategory
- **assistance**: Model Functional Test Suite re-written to pytest for model KnowledgeBase
- **assistance**: API Fields Render Functional Test Suite re-written to pytest for model KnowledgeBase
- **api**: SubModel ViewSet Test Suite to test re-written class
- **api**: Dont test a django object that has not been customised
- **access**: Initial ViewSet Unit Test Suite for Entity Model
- **access**: Add Serializer unit test suit for model Role
- **access**: Add Serializer unit test suit for model Person
- **access**: Add Serializer unit test suit for model Entity
- **access**: Add Serializer unit test suit for model Contact
- **access**: Add Serializer unit test suit for model Company
- **itim**: Refactor TicketSLM model API Fields render test Suite to PyTest
- **itim**: Refactor TicketRequest model API Fields render test Suite to PyTest
- **core**: Refactor TicketBase model API Fields render test Suite to PyTest
- **api**: Refactor Test Suite for API Fields render tests to PyTest
- **itam**: Refactor ITAMAssetBase model API Fields render test Suite to PyTest
- **accounting**: Refactor AssetBase model API Fields render test Suite to PyTest
- **core**: Refactor TicketCommentSolution model API Fields render test Suite to PyTest
- **core**: Refactor TicketCommentAction model API Fields render test Suite to PyTest
- **core**: Refactor TicketCommentBase model API Fields render test Suite to PyTest
- **human_resources**: Refactor Employee model API Fields render test Suite to PyTest
- **access**: Refactor Person model API Fields render test Suite to PyTest
- **access**: Refactor Entity model API Fields render test Suite to PyTest
- **access**: Refactor Contact model API Fields render test Suite to PyTest
- **access**: Refactor Company model API Fields render test Suite to PyTest
- **devops**: Adjust functional model test to use fixture kwargs
- Ensure when obj created via serializer calls full_clean
- Ensure Clean methods called
- Test case for model field type
- **fixture**: if item already exists, when fetching remove modified field from query if not found with
- **access**: Model Role is not usable within global org, remove test
- **devops**: skip Model History entry test as it should be done as part of serializer and viewset
- **devops**: update no_org_serializer test so it works for model SoftwareEnableFeatureFlag
- **itam**: Model DeviceOperatingSystem is not multi-org based skip those tests
- **settings**: Model UserSettings does not allowing adding rows, skip test
- **settings**: Model AppSettings does not allowing adding rows, skip test
- **fixture**: Ensure _meta attribute exists when cleaning up models prior to attempting to use
- **devops**: SoftwareEnableFeatureFlagging model does not use global org, so dont test global org return
- **api**: when testing create object, remove the actual created object prior to testing the add
- **fixture**: when creating object and it exists, rtn that object
- **devops**: If test publically accessable, dont test by user org only as test is NA
- **settings**: UserSettings perms tests are for the user that is accessing them
- **settings**: UserSettings perms tests are not org based, skip those tests
- **settings**: AppSettings perms tests are not org based, skip those tests
- **settings**: for api checks for model AppSettings, make user super_user
- **settings**: Exclude inter-org tests for model AppSettings
- **settings**: Remove old API Permission tests no longer required
- **settings**: Ensure ExternalLink model hasrequired field template added
- **api**: if model lacks list endpoint, check if method alllowed for test cases for Functional API perms test suite
- **api**: if model lacks organization field, xfail returned orgs test cases for Functional API perms test suite
- Ensure service fixture assosiates with device
- **api**: if model lacks organization field, xfail returned orgs test cases for Functional API perms test suite
- Add depreciated models to be excluded from coverage
- **api**: Update Functional API Permission test suite to cater for public RO endpoints
- **core**: Ensure model mehod `get_url_kwargs` returns a dict for all Centurion Models
- **devops**: Add GitLabRepository Unit Model test suite
- **devops**: Add GitHubRepository Unit Model test suite
- **devops**: Add GitRepository Unit Model test suite
- **devops**: Add Checkin Unit Model test suite
- **devops**: correct GitGroup Unit model test suite
- **devops**: correct FeatureFlag Unit model test suite
- **core**: Add TicketCommentCategory Unit model test suite
- **core**: Add TicketCategory Unit model test suite
- **core**: Add Manufacturer Unit model test suite
- **access**: Add Tenant Unit serializer test suite
- Add initial unit serializer test suite
- **access**: Update Tenant URL route basename again
- **itam**: Updated Unit model test for Device Model
- **access**: Update Tenant URL route basename
- **access**: Tenant Model Tests
- **api**: Update Functional API Permissions to support listview models with kwargs
- **api**: exclude model `ConfigGroupHosts` from api permission tests as it has no endpoint
- **api**: API Permissions Functional test to supprt name as unique field
- **config_management**: Completed ConfigGroupSoftware Model Tests
- **config_management**: Completed ConfigGroup Model Tests
- **config_management**: Completed ConfigGroupHost Model Tests
- **core**: mock the user object within the model context
- **core**: creating a model is a functional not unit test
- **devops**: re-implement temp removed test suites.
- **api**: API Permissions Auto-Creator test suite
- **devops**: Add GitGroup API Permissions tests
- **core**: Add fixtures for api permission tests
- **core**: rewrite api permissions test suite to use pytest and fixtures
- **core**: Ensure Method clean_fields functions for CenturionNotesModel
- **core**: Function Model test suite for CenturionModelNote Meta Models
- **core**: Interim Unit Model test suite for CenturionModelNote  Meta Models
- **core**: Interim Unit Model test suite for CenturionModelNote
- **core**: Dynamic Unit Test Suites for Meta Models AuditHistory
- **core**: Unit Test Centurion Model method `__str__`
- **core**: Unit Test Centurion Model method `get_url_kwargs`
- **core**: Unite Tesxt Centurion Model method `get_url` attr `_is_submodel` set
- **core**: Unite Tesxt Centurion Model method `get_url` attr `model_name` set
- **core**: Ensure model that has audit enableed has audit model
- **core**: Add Functional  model Test Suite for CenturionAuditModel
- **devops**: Ensure that a Github group cant have a parent/"be nested"
- **devops**: Ensure that when create a child git group that the tenancy matches the parent git group
- **devops**: Add Functional  model Test Suite
- **core**: Add Base Centurion model Functional Test Suite
- **access**: Add Base Tenancy model Functional Test Suite
- **base**: Add Base model Functional Test Suite
- **core**: Model Unit Tests for AuditHistory `get_model_history` method
- **core**: reset vals so as not to fuck other tests over
- **core**: Correct test for method `get_audit_values` for `CenturionAbstractModel`
- **devops**: Initial Model Unit tests for GitGroup
- **core**: Add field `model_notes` as an excluded field for AuditModels
- **core**: Remaining Unit Model Test Cases for CenturionAuditMeta Model
- **core**: Initial Unit Model Test Cases for CenturionAuditMeta Model
- **core**: Unit Model Test Cases for CenturionSubAbstract model
- **core**: Initial Unit Model Test Cases for CenturionAudit Model
- **core**: Unit test cases for Centurion get_url relative + non-relative
- **access**: Unit Model Tests for TenancyAbstractModel
- **base**: Unit Common Model test cases suite
- **base**: Unit Common Class test cases suite
- **access**: Unit Model Tests for TenancyAbstractModel

## 1.18.0 (2025-07-03)

### feat

- **python**: upgrade django 5.1.9 -> 5.1.10

### Fixes

- **itim**: Correct config that is in the incorrect format

## 1.17.1 (2025-06-02)

### Fixes

- **base**: Add python metrics to prometheus exporter

## 1.17.0 (2025-05-16)

### feat

- **access**: model access.Company feature flag `2025-00008`
- **access**: URL route for model access.Company
- **access**: Migration for model access.Company
- **access**: Serializer for model access.Company
- **access**: New model access.Company
- **access**: Organization -> Tenant Permission Migration
- **docker**: Serve a robots.txt file for NO indexing
- **access**: Organization -> Tenant Permission Migration
- **base**: Add var `AUTH_USER_MODEL` to settings
- **core**: Add Action comments on ticket change
- **core**: Remove add, change and delete permissions for model TicketCommentAction from permission selector
- **core**: Serializer for model TicketCommentAction
- **core**: Migrations for model TicketCommentAction
- **core**: New model TicketCommentAction
- **core**: Setup serializer to meet requirements
- **core**: Setup model to meet requirements
- **api**: Add exception logging to ViewSetCommon
- **python**: Upgrade DRF Spectacular 0.27.2 -> 0.28.0
- **python**: Upgrade DRF 3.15.2 -> 3.16.0
- **core**: When processing slash command duration, cater for new ticket models
- **api**: Add Logging function to Common ViewSet
- **access**: Add Logging function to Tenancy model
- **base**: Enable user to customize log file location
- **core**: Do validate the comment_type field for TicketCommentBase
- **itam**: Add Feature Flag `2025-00007` ITAMAssetBase
- **itam**: Add endpoint for ITAMAssetBase
- Model tag migration for Asset and IT Asset
- **itam**: Model tag for ITAsset
- **accounting**: Model tag for Asset
- **accounting**: Add app label to kb articles for notes
- **accounting**: Migrations for notes model for AssetBase
- **accounting**: Migrations for history model for AssetBase
- **accounting**: Notes Viewset for AssetBase
- **accounting**: Notes Serializer for AssetBase
- **accounting**: Notes model for AssetBase
- **accounting**: History model for AssetBase
- **itam**: Serializer for ITAssetBase
- **itam**: Migrations for ITAssetBase
- **itam**: Add Model ITAssetBase
- **accounting**: Viewset for Assets
- **accounting**: Serializer for model AssetBase
- **accounting**: Migrations for model AssetBase
- **accounting**: Add Model AssetBase

### Fixes

- **api**: Dont try to access attribute if not exist in common viewset
- **api**: Dont try to access attribute if not exist in common viewset
- **api**: Correct ViewSet Sub-Model lookup
- **core**: Only take action on ticket comment if view exists
- **api**: Ensure multi-nested searching for sub-models works
- **core**: ensure slash command is called on ticket description
- **core**: Spent slash command is valid for time spent
- **core**: Correct logic for TicketCommentSolution
- **core**: Correct logic for TicketCommentBase
- **accounting**: Ensure correct sub-model check is conducted within model type
- **itam**: ensure RO field asset_type is set
- **itim**: Ensure that itam base model is always imported

### Refactoring

- **human_resources**: Update Functional ViewSet to use PyTest for Employee Model
- **Access**: Update Functional ViewSet to use PyTest for Person Model
- **Access**: Update Functional ViewSet to use PyTest for Entity Model
- **Access**: Update Functional ViewSet to use PyTest for Contact Model
- **Access**: Update Functional Permission to use PyTest for Person Model
- **Access**: Update Functional Permission to use PyTest for Entity Model
- **Access**: Update Functional Permission to use PyTest for Contact Model
- **Access**: Update Functional Serializer to use PyTest for Contact Model
- **Access**: Update Functional Serializer to use PyTest for Entity Model
- **Access**: Update Functional Serializer to use PyTest for Person Model
- **human_resources**: Update Functional Serializer to use PyTest for Employee Model
- **human_resources**: Update Functional Permissions to use PyTest for Employee Model
- **human_resources**: Update Functional Metadata to use PyTest for Employee Model
- **access**: Update Functional Metadata to use PyTest for Person Model
- **access**: Update Functional Metadata to use PyTest for Entity Model
- **access**: Update Functional Metadata to use PyTest for Contact Model
- **access**: Update Model Entity to use PyTest for Model Test Suite
- **access**: Update Model Contact to use PyTest for Model Test Suite
- **access**: Update Model Person to use PyTest for Model Test Suite
- **human_resources**: Update Model Employee to use PyTest for Model Test Suite
- **human_resources**: Update Model Employee to use PyTest API Fields Render
- **access**: Update Model Person to use PyTest API Fields Render
- **access**: Update Model Contact to use PyTest API Fields Render
- **access**: Update Model Entity to use PyTest API Fields Render
- **access**: Rename model Organization -> Tenant
- **settings**: Update all references to `User` to use `get_user_model()`
- **project_management**: Update all references to `User` to use `get_user_model()`
- **itam**: Update all references to `User` to use `get_user_model()`
- **devops**: Update all references to `User` to use `get_user_model()`
- **core**: Update all references to `User` to use `get_user_model()`
- **config_management**: Update all references to `User` to use `get_user_model()`
- **assistance**: Update all references to `User` to use `get_user_model()`
- **app**: Update all references to `User` to use `get_user_model()`
- **api**: Update all references to `User` to use `get_user_model()`
- **accounting**: Update all references to `User` to use `get_user_model()`
- **access**: Update all references to `User` to use `get_user_model()`
- **access**: when fetching parent object, use the parent_model get function
- **api**: Limit url pk regex to ensure the value is a number

### Tests

- **access**: Functional ViewSet Test Suite Company model
- **access**: Functional Serializer Test Suite Company model
- **access**: Functional Permissions Test Suite Company model
- **access**: Functional MetaData Test Suite Company model
- **access**: ViewSet Test Suite Company model
- **access**: API field render Test Suite Company model
- **access**: Model Test Suite Company model
- **core**: Unit viewset Test Cases for TicketCommentAction model
- **core**: Unit model Test Cases for TicketCommentAction model
- **core**: Unit API Render Test Cases for TicketCommentAction model
- **core**: Interim Functional model Test Case TicketCommentAction
- **core**: Ensure that a ticket milestone comes from the same assigned project
- **core**: SKIP Tests TicketBase Description Slash command Checks
- **core**: TicketBase Description Slash command Checks
- **core**: TicketBase Remaining Serializer Chacks
- **core**: Partial functional Model Test Suite covering some slash commande for TicketCommentSolution
- **core**: ensure ticket is un-solved for ticketcomment unit api render fields check
- **core**: ensure slash command is called on ticket comment
- **core**: Unit ViewSet Test Suite for TicketCommentSolution
- **core**: Unit ViewSet Test Suite for TicketCommentBase
- **core**: Skip Related slash command checks until migrating tickets to new model
- **core**: Add ability to unit api field rendering test case for second api request if required
- **core**: Partial Functional Model test cases (Slash Commands) for TicketCommentBase
- **core**: Functional Model test cases (Slash Commands) for TicketBaseModel
- **core**: Partial Slash Command re-write
- **core**: correct field so its valid for unit TicketCommentBase model
- **core**: Unit API Fields Render for TicketCommentSolution model
- **core**: Unit API Fields Render for TicketCommentBase model
- **core**: Unit Model assert save and call are called for TicketBase
- **core**: Unit Model Checks for TicketCommentSolution
- **core**: Unit Model Checks for TicketCommentBase
- **itam**: test meta attribute itam_sub_model_type for ITAMBaseModel
- **itam**: Dont use constants where variables should be used
- **itam**: Remaining Unit Model test cases for AssetBase
- **accounting**: Remaining Unit Model test cases for AssetBase
- **itam**: Functional ViewSet Test Cases for ITAMAssetBase
- **itam**: Functional Serializer Test Cases for ITAMAssetBase
- **itam**: Functional Permissions Test Cases for ITAMAssetBase
- **itam**: Functional Metadata Test Cases for ITAMAssetBase
- **itam**: Functional History Test Cases for ITAMAssetBase
- **accounting**: Functional ViewSet Test Cases for AssetBase
- **accounting**: Functional Serializer Test Cases for AssetBase
- **accounting**: Functional Permissions Test Cases for AssetBase
- **accounting**: Functional Metadata Test Cases for AssetBase
- **accounting**: History Test Cases for AssetBase
- add missing merge of add_data for api permissions tests
- remove ticket only vars from api permissions tests
- **api**: dont use constants for variable data
- correct viewset tests
- **itam**: Unit Viewset checks for AssetBase Model
- **core**: Add missing fields is_global checks for ticket base
- **api**: Add submodel url resolution for metadata
- **itam**: Unit API Fields checks for ITAM AssetBase Model
- **accounting**: Unit API Fields checks for AssetBase Model
- Support variables that were defined as properties.
- **api**: Ensure that model notes is added to model create for api field tests
- **accounting**: Unit Viewset checks for AssetBase Model
- **itam**: Unit Model checks for ITAMAssetBase Model
- **base**: update Model base test suite for model_notes field
- **accounting**: Unit Model checks for AssetBase Model

## 1.16.0 (2025-05-04)

### feat

- **core**: Add ViewSet for Ticket Comments
- **project_management**: Depreciate Project Task Ticket Endpoint
- **itim**: Depreciate Problem Ticket Endpoint
- **itim**: Depreciate Incident Ticket Endpoint
- **itim**: Depreciate Change Ticket Endpoint
- **assistance**: Depreciate Ticket Comment
- **assistance**: Depreciate Request Ticket Endpoint
- **core**: Add routes for Ticket Comments
- **core**: update ticket serializer to use new comment base url
- **core**: Add permissions `import`, `purge` and `triage` to model TicketCommentSolution
- **core**: Add permissions `import`, `purge` and `triage` to model TicketCommentBase
- **core**: Filter ticket_comment_model routes to those defined in `Meta.sub_model_type`
- **core**: Filter ticket_model routes to those defined in `Meta.sub_model_type`
- **access**: Filter entity_model routes to thos defined in `Meta.sub_model_type`
- **core**: Serializer for TicketCommentBase
- **core**: Serializer for TicketCommentSolution
- **core**: Ticket Comment Get URL functions
- **core**: Ticket Comment Validation for comment_type
- **core**: Update choices fields for TicketCommentBase model
- **core**: init for model TicketCommentSolution
- **core**: Migrations for choice fields for TicketBase model
- **core**: Migrations for model TicketCommentSolution
- **core**: Update choice fields for TicketBase model
- **core**: New model TicketCommentSolution
- **api**: when fetching related_object, default to base_model for SubModelViewSet
- Add field `Meta.sub_model_type` to sub-models
- **core**: New interim model TicketCommentSolution
- **core**: add ticket routes
- **itim**: serializer for SLMTicketBase
- **itim**: Serializer for RequestTicket
- **itim**: migrations for RequestTicket
- **itim**: New Model RequestTicket
- **itim**: migration for SLMTicketBase
- **itim**: New Model SLMTicketBase
- **core**: migrations for TicketCommentBase
- **core**: New Model TicketCommentBase
- **core**: viewset for TicketBase
- **core**: serializer for TicketBase
- **core**: migrations for TicketBase
- **core**: New Model TicketBase
- **project_management**: add estimation field to project api fields
- **human_resources**: nav menu entries for Employee
- **human_resources**: Serializer for Employee
- **human_resources**: Migration for Employee
- **human_resources**: New model Employee
- **devops**: add missing api index menu entry for devops
- **access**: add missing nav menu entries for entities
- **human_resources**: add module to perms selector

### Fixes

- **test**: correct typo in attribute parameterized_
- **core**: Ticktet comment can have empty body
- **core**: If model does not save history, dont attempt to cache before
- **itam**: provide return_url as part of software version meta
- **itim**: correct ticket_slm serializer
- **itim**: correct ticket_request serializer
- **api**: SubModelViewSet.related_objects must be the same class as the base model
- **access**: Ensure related model is a sub-model
- **human_resources**: Correct history link generation and add docs
- **human_resources**: Correct history link generation
- **access**: add missing attribute to Tenancy object

### Refactoring

- **test**: rewrite model unit tests to use PyTest
- **test**: Update test parameterization
- **api**: SubModelViewSet must inherit from ModelViewSet as it's an extension
- **core**: rename ticket model filename in preparation for base ticket model
- **access**: migrate sub-model viewset logic to common
- **project_management**: add duration field to project api fields
- **human_resources**: Move employee details to its own section

### Tests

- **core**: Serializer Validation for ticket status change for TicketBase model
- **core**: Prevent Closing / Solving of TicketBase Model if not ready
- **itim**: Incomplete Model Unit Tests for RequestTicket
- **itim**: Incomplete Model Unit Tests for SLMTicketBase
- **core**: Incomplete Model Unit Tests for TicketBase
- **itim**: RequestTicket Updated, yet incomplete Test Suite for Serializer
- **itim**: SLMTicketBase Updated, yet incomplete Test Suite for Serializer
- **core**: TicketBase Updated, yet incomplete Test Suite for Serializer
- Correct Test Suite for Serializer for models TicketBase, TicketRequest and TicketSLM
- **itim**: RequestTicket Initial Test Suite for Serializer
- **itim**: SLMTicket Initial Test Suite for Serializer
- **core**: TicketBase Initial Test Suite for Serializer
- **core**: SLMTicket Test Suite for ViewSet
- **core**: SLMTicket Test Suite for Metadata
- **core**: Request Test Suite for ViewSet
- **core**: Request Test Suite for Metadata
- **core**: TicketBase Test Suite for ViewSet
- **core**: TicketBase Test Suite for Metadata
- **api**: update test cases for SubModelViewSet Base Test Class
- **itim**: RequestTicket ViewSet Test Suite
- **core**: TicketBase ViewSet Test Suite
- **api**: Incomplete SubModelViewSet Test Cases
- **api**: SubModelViewSet Test Suite Setup
- correct tests from Meta.sub_model_type changes
- correct serializer imports from recent file renames
- Fixture for creating model with random data
- **itim**: API Field checks for TicketSLMBase
- **itim**: API Field checks for TicketRequest
- **core**: API fields Tests for TicketBase
- **core**: API fields Unit Test Suite
- **core**: Correct model notes test suite
- **core**: API Permission Test Cases for ticket_base model
- **api**: add API Permission Test Cases
- **access**: Correct history link test cases
- **project_management**: Add test cases for api field render for model fields `estimation_project` and `duration_project`
- **human_resources**: History Serializer and ViewSet Functional test suites for employee
- **human_resources**: APIv2, History, Model and ViewSet Unit test suites for employee
- Migrate models to use refactored model tests
- Consolidate All model tests to remove duplicates and to simplify

## 1.15.1 (2025-04-10)

### Fixes

- **python**: Downgrade django 5.2 -> 5.1.8

## 1.15.0 (2025-04-10)

### feat

- **settings**: Move Ticket Comment Category from settings to ITOps menu
- **settings**: Move Ticket Category from settings to ITOps menu
- **access**: place roles nav behind feature flag 2025-00003
- **access**: place directory nav behind feature flag 2025-00002
- **accounting**: add new module
- **access**: Ensure that the same person cant be created more than once
- **access**: Place Roles Model behind feature flag `2025-00003`
- **access**: When querying permissions, select related field `content_type`
- **core**: Model tag for Access/Role
- **access**: Model Role notes endpoint
- **access**: Add navigation entry for roles
- **access**: Model Role History migrations
- **access**: Add model Role History
- **access**: Role Notes model viewset
- **access**: Role Notes model serializer
- **access**: Model Role Notes migrations
- **access**: Add model Role Notes
- **access**: Role model viewset
- **access**: Role model serializer
- **access**: Model Role migrations
- **access**: Add model Role
- **python**: Upgrade Django 5.1.7 -> 5.2
- **access**: Place Entity URLs behind feature flag `2025-00002`
- **access**: Add detail page layout for contact model
- **access**: Add Menu entry for corporate directory
- **access**: Add back_url to Entity metadata
- **core**: Add Entity model tag
- **access**: Update Entity field `entity_type` if it does not match the entity type
- **access**: All Entity models to use the entity history endpoint
- **access**: Enable specifying the history model to use for audit history for a model
- **access**: Enable specifying the kb model to use for linking kb article to a model
- **access**: All Entity models to use the entity notes endpoint
- **access**: Enable specifying the notes `basename` for a model
- **access**: ViewSet for Entity Notes model
- **access**: Serializer for Entity Notes model
- **access**: new model Entity Notes
- **access**: New model Entity History
- **access**: Add Entity URL routes
- **access**: new serializer Contact
- **access**: new model Contact
- **access**: new serializer Person
- **access**: new model Person
- **access**: new ViewSet for for Entity and sub-entities
- **access**: new serializer Entity
- **access**: new model Entity
- **human_resources**: Add navigation menu entry for Human Resources (HR)
- **human_resources**: Add module Human Resources (HR) to API Urls
- **base**: Add module Human Resources (HR) to installed apps
- Add module Human Resources (HR)

### Fixes

- **api**: Correct documentation link to use models verbose name
- **feature_flag**: cater for settings flag overrides
- **access**: Add missing field directory to contact model
- **settings**: Add Application Settings to Admin page
- **access**: Remove app_namespace from Entity
- **access**: add missing tenancy object fields to non-tenancy object models
- **core**: Dont attempt to fetch history related objects if no history exists
- **api**: Dont attempt to access kwargs if not exists within common serializer

### Refactoring

- **core**: When saving history, ensure field `_prefetched_objects_cache` is not included

### Tests

- **settings**: Correct nav menu entry for Ticket Category and Ticket Comment Category
- **access**: Ensure Model Contacts inherits from Person Model
- **access**: Functional Test Suite for Contact API Metadata, API Permissions and ViewSet
- **access**: Functional Test Suite for Contact serializer
- **access**: Functional Test Suite for Contact history
- **access**: Correct Entity and person functional Test Suite so sub-model testing works
- **access**: Correct table_fields test case to cater for dynamic field
- **access**: Unit Test for Contact ViewSet
- **access**: Unit Test for Contact model
- **access**: Unit Test for Contact history API field checks
- **access**: Unit Test for Contact API field checks
- **access**: Unit Test for Person Tenancy Object
- **access**: Correct Entity and person unit Test Suite so sub-model testing works
- **access**: Entity Function Serializer test cases
- **access**: Person Model field test cases
- **access**: Functional Test for Person ViewSet, Permissions and Metadata
- **access**: Functional Test for Person History
- **access**: Correct Entity Function Test Suite so sub-model testing works
- **access**: Unit Test for Person ViewSet
- **access**: Unit Test for Person Model
- **access**: Unit Test for Person History API fields
- **access**: Unit Test for Person API fields
- **access**: Unit Test for Person Tenancy Object
- **access**: Correct Entity Test Suite so sub-model testing works
- **app**: exclude any field check that ends in `_ptr_id`
- **access**: Remove teardown from Function Test cases for Role serializer
- **access**: Test cases for Role serializer
- **access**: Function Test cases for Role SPI Permissions, ViewSet and Metadata
- **access**: Function Test cases for Role History
- **access**: Unit Test case to ensure Role is by organization
- **access**: Unit Test case to ensure Role cant be set as global object
- **access**: Unit Test cases for Role ViewSet
- **access**: Unit Test cases for Role model
- **access**: Unit Test cases for Role History API v2
- **access**: Unit Test cases for Role API v2
- **access**: Unit Test cases for Role Tenancy Object
- During testing add debug_feature_flags so object behind can be tested
- **access**: Notes ViewSet Functional Tests for Entity Model
- **access**: Notes API Field Functional Tests for Entity Model
- **access**: Correct functional ViewSet test suite for Entity model
- **access**: History functional Tests for Entity model
- **access**: PermissionsAPI, ViewSet and Metadata Tests for Entity model
- **access**: Model test cases for Entity
- **access**: API Rendering test cases for Entity model
- **api**: Ensure that when mocking the request the viewset is instantiated
- **access**: History tests for Entity model
- **access**: ViewSet tests for Entity model
- **access**: Tenancy object test for Entity model

## 1.14.0 (2025-03-29)

### feat

- **itops**: Add navigation menu
- New Module ITOps
- **devops**: Ensure GitHub Groups can't be nested
- **devops**: Models  Git Repository must use organization from `git_group` as must group if parent set
- **devops**: Add git provider badge to git_group table fields
- **devops**: Add git provider badge to git_repository table fields
- **devops**: Add Git GRoup to navigation
- **itam**: Add `back_url` to Software Version ViewSet
- **itam**: Add `back_url` to Operating System ViewSet
- **devops**: Add `page_layout` to Git Group model
- **devops**: Add `page_layout` to GitLab repository model
- **devops**: Add `page_layout` to GitHub repository model
- **devops**: git_repository ViewSet updated to fetch queryset based off of repository provider
- **devops**: Add ti git_repository ViewSet return and back urls
- **devops**: Make fields `provider` and `provider_id` unique_together for git_repository model
- **devops**: Add fields to ALL git_repository serializers
- **devops**: Add fetching of URL to base git_repository model
- **api**: Enable fetching of app_namespace from model
- **access**: Add function get_page_layout
- **feature_flag**: Provide user with ability to override feature flags
- **base**: Add middleware feature_flag
- **devops**: Disable notes for GIT Repository Base Model
- **devops**: Add git_repository model tag migration
- **devops**: Add git_repository as a model that can be linked to a ticket
- **devops**: Git Group Notes Migration
- **devops**: Git Group Notes ViewSet
- **devops**: Git Group Notes Serializer
- **devops**: Git Group Notes Model
- **devops**: GitHub and GitLab Repository Notes Migrations
- **devops**: GitLab Repository Notes Viewset
- **devops**: GitHub Repository Notes Viewset
- **devops**: GitLab Repository Notes Serializer
- **devops**: GitHub Repository Notes Serializer
- **devops**: GitLab Repository Notes Model
- **devops**: GitHub Repository Notes Model
- **devops**: Git Group History Migrations
- **devops**: Git Group History
- **devops**: GitLab and GitHub Repository History Migrations
- **devops**: GitLab Repository History
- **devops**: GitHub Repository History
- **devops**: [2025-00001] Git Group and Repositories URLs
- **devops**: Git Group and Repositories Migrations
- **devops**: GIT Group ViewSet
- **devops**: GIT Group Serializer
- **devops**: GIT Group Model
- **devops**: GIT Repositories Viewset
- **devops**: GitLab Serializer for git repositories
- **devops**: GitHub Serializer for git repositories
- **devops**: Base Serializer for git repositories
- **devops**: GitLab Repository Model
- **devops**: GitHub Repository Model
- **devops**: Base model for git repositories
- **core**: Enable slash command related ticket to have multiple ticket references
- **core**: Enable slash command linked model to have multiple models
- **core**: process ticket slash commands by line
- **core**: Migrations for new slash commands
- **project_management**: Add project_state slash command
- **core**: Add ticket_comment_category slash command
- **core**: Add ticket_category slash command
- **itam**: when displaying software version, add prefix with software name
- **itam**: Add markdown tag $software_version
- **itam**: Enable ticket tab on software version page

### Fixes

- **devops**: Correct git_group serializer parameter name
- **devops**: Correct field path to no be unique for git_repository
- **feature_flag**: if over_rides not set ensure val set to empty dict
- **devops**: git_group serializers must define fields
- **devops**: git_group serializers must return urls
- **devops**: Correct git_repository notes urls
- **devops**: Correct git_repository url regex
- **devops**: Correct ViewSerializer for GitLab Repository
- **devops**: Correct ViewSerializer for GitHib Repository
- **devops**: Correct model git_group modified field name part 2
- **devops**: Correct model git_group modified field name
- **api**: Fetching of serializer_class must be dynamic
- **core**: Don't create an empty ticket comment if the body is empty when slash commands removed
- **core**: when processing slash commands trim each line prior to processing
- **core**: slash command NL char is `\r\n` not `\n`, however support both
- **core**: When processing slash commands trim whitespace on return
- **core**: Ensure linked ticket models are unique
- **itam**: Add back url to software_version model

### Refactoring

- **devops**: remove model unique_together constraint for git group and repository
- **devops**: Field `provider_id` must not be user editable for git group or repository
- **api**: mv _nav property to function get_nav_items

### Tests

- **api**: Correct test cases for view_name and view_description
- Refactor all ViewSet Unit Test cases to use new test cases class
- **api**: Common ViewSet classes Tests and Test cases for classes that inherit them
- **api**: correct nav menu setup to use mock request
- **core**: un-mark tests as skipped so that multiple linked items per ticket can be tested
- **core**: correct ticket linked item to prevent duplicate creation

## 1.13.1 (2025-03-17)

### Fixes

- **devops**: After fetching feature flags dont attempt to access results unless status=200
- **docker**: only download feature flags when not a worker
- **devops**: Use correct stderr function when using feature_flag management command
- **devops**: Cater for connection timeout when fetching feature flags
- when building feature flag version, use first 8 chars of build hash

### Refactoring

- **docker**: Use crontabs not cron.d

## 1.13.0 (2025-03-16)

### feat

- **devops**: Add ability for user to turn off feature flagging check-in
- **devops**: When displaying the feature_flag deployments, limit to last 24-hours
- **devops**: During feature flag `Checkin` derive the version from the last field of the user-agent
- **devops**: Add missing column to model `Checkin`
- **devops**: Remove model `Checkin` permissions from permissions selector
- **devops**: Display the days total unique check-ins for feature flags within software feature flagging tab
- **devops**: Record to check-in table every time feature flags are obtained
- **devops**: Migrations for model `CheckIns`
- **devops**: New model `CheckIns`
- Generate a deployment unique ID
- **devops**: Provide user with option to disable downloading feature flags
- **devops**: Feature Flagging url.path wrapper
- **docker**: Configure cron to download feature flags every four hours
- **docker**: Start and run crond within container
- **docker**: Download feature flags on container start
- **devops**: Feature Flagging DRF Router wrapper
- **devops**: Feature Flagging middleware
- **devops**: Feature Flagging management command
- **devops**: Add Feature Flagging lib
- **devops**: add temp application for feature flag client
- **devops**: public feature flag endpoint pagination limited to 20 results
- **devops**: Add support for `if-modified-since` header for Feature Flags public endpoint
- **api**: Add public API feature flag index endpoint
- **api**: Add public API endpoint
- **devops**: Add feature flag public ViewSet
- **devops**: Add feature flag public serializer
- **api**: Add common viewset for public RO list
- Remove serializer caching from ALL viewsets
- **devops**: Add delete col to software enabled feature flags
- **devops**: Prevent deletion  of software when it has feature flagging enabled and/or feature flags
- **devops**: limit feature_flag to organizations that's had feature flags enabled
- **devops**: limit feature_flag to software that's had feature flags enabled
- **python**: Update Django 5.1.5 -> 5.1.7
- **devops**: Serializer limiting of software and os disabled for time being
- **devops**: Serializer validate software and org
- **devops**: Serializer software filter to enabled feature_flag software
- **devops**: Serializer org filter to enabled feature_flag organizations
- **devops**: Add endpoint for enabling software for feature flagging
- **devops**: Add serializer for enabling software for feature flagging
- **devops**: Add model for enabling software for feature flagging
- **devops**: Add model tag feature_flag to ticket linked item
- **devops**: Add KB tab to feature flag model
- **devops**: Add Notes to feature flag model
- **core**: Migration for feature_flag model reference
- **core**: url endpoints added for ticket comment category and ticket category notes
- **itam**: disable model notes for model device os
- **api**: disable model notes for model auth token
- **core**: disable model notes for model teamuser
- **core**: disable model notes for model notes
- **core**: Migrations for adding notes to ticket category and ticket comment category
- **core**: Add Feature Flag model reference
- **devops**: Add devops module to installed applications
- **devops**: Add Feature Flag viewset
- **devops**: Add Feature Flag serializer
- **devops**: Add devops Navigation menu
- **devops**: Add devops module URL includes
- **devops**: Add devops to permissions
- **devops**: DB Migrations for Feature Flag and History model
- **devops**: Add Feature Flag History model
- **devops**: Add Feature Flag model
- **access**: add support for nested application namespaces
- **devops**: Add devops module

### Fixes

- **devops**: Only track checkin if no other error occured
- **devops**: during feature flag checkin, if no `client-id` provided, use value `not-provided`
- **devops**: When init the feature flag clients, look for all args within settings
- **devops**: Only add `Last-Modified` header to response if exists
- **devops**: Correct logic for data changed check for public endpoint for feature flagging
- **devops**: feature flag public ViewSet serializer name correction and qs cache correction
- **devops**: feature flag public endpoint field modified name typo
- **devops**: Filter public feature flag endpoint to org and software where software is enabled
- **devops**: Move software field filter for feature flag to the serializer
- **devops**: Dont attempt to validate feature flag software or organization if it is absent
- **devops**: Correct feature flagging validation for enabled software and enabled orgs
- **devops**: dont cache serializer for featureflag
- **devops**: Correct Feature Flag serializer validation to cater for edit
- **devops**: Feature Flag field is mandatory
- **api**: make history url dynamic. only display if history should save
- **devops**: if software is deleted delete feature flags
- **core**: disable of notes for models not requiring it
- **api**: when generating notes url, use correct object
- **api**: Add missing import for featurenotused
- **core**: Add ability to add notes for ticket comment category
- **core**: Add ability to add notes for ticket category
- **core**: Serializer `_urls.notes` URL generation now dynamic
- **api**: Dont attempt to access model.get_app_namespace if it doesnt exist

### Tests

- **devops**: Feature Flag History API render checks
- **devops**: Feature Flag Serializer checks
- **devops**: CheckIn Entry created of fetching feature flags
- **devops**: CheckIn model test cases
- **devops**: public feature flag fields corrections
- **devops**: public feature flag functional ViewSet checks
- **devops**: feature flag ViewSet checks
- **api**: Update vieset test cases to cater for mockrequest to contain headers attribute
- **devops**: feature flag public endpoint API field, header checks
- **devops**: Ensure that only enabled org and enabled software is possible
- **devops**: software_feature_flag_enable ViewSet checks
- **devops**: software_feature_flag_enable Serializer checks
- **devops**: Update feature flag test case setup to enable feature flag for testing software
- **devops**: Update feature flag test case setup to enable feature flag for testing software
- **api**: Remove serializer cache test cases
- **devops**: software_feature_flag_enable api field checks
- **devops**: software_feature_flag_enable viewset checks
- **devops**: software_feature_flag_enable model checks
- **devops**: software_feature_flag_enable tenancy object checks
- **devops**: correct dir name for tests
- **devops**: Notes feature flag model checks
- **core**: Ticket Comment Category Notes checks
- **core**: Ticket Category Notes checks
- **app**: Model test cases for api field rendering `_urls.notes`
- **app**: Model test cases for get_url_kwargs_notes function
- **access**: Correct Team notes url route name
- **devops**: Feature Flag viewset unit Checks
- **devops**: Feature Flag model Checks
- **devops**: Feature Flag api Checks
- **devops**: Feature Flag tenancy object Checks
- **devops**: Feature Flag viewset functional Checks
- **devops**: Feature Flag serializer Checks
- **devops**: Feature Flag History Checks

## 1.12.0 (2025-03-01)

### feat

- **api**: Add delete column to AuthToken Table
- **docker**: Upgrade system packages on build
- **api**: AuthToken requires viewset get_back_url
- **api**: Add auth token api endpoint
- **settings**: Add section title to auth tokens
- **settings**: Add tokens url to user settings `_urls`
- **api**: Update Auth Token model for use with serializer
- **api**: Add user Auth Token viewset
- **api**: Add user Auth Token serializer
- **settings**: Add `page_layout` attribute to User Settings

### Fixes

- **api**: correct usage of `AuthToken.generate` to a property

### Tests

- **api**: AuthToken ViewSet checks (unit)
- **api**: AuthToken API Field checks
- **api**: AuthToken Serializer checks
- **api**: AuthToken ViewSet checks

## 1.11.0 (2025-02-21)

### feat

- **core**: Enable App settings History to save without specifying an organization
- **settings**: save_history method added to App Settings
- **settings**: History Model for App Settings Version added
- **core**: Migration for history data to new history tables
- **access**: save_history method added to Team
- **access**: History Model for Team added
- **access**: save_history method added to Organization
- **access**: History Model for Organization added
- **core**: add org field History Model api rendering
- **core**: Show the model name within history
- **project_management**: Project Milestone added to modelhistory.child_history_models
- **settings**: History Model migrations for External Link
- **settings**: save_history method added to External Link
- **settings**: History Model for External Link added
- **project_management**: History Model migrations for Project Type
- **project_management**: save_history method added to Project Type
- **project_management**: History Model for Project TYpe added
- **project_management**: History Model migrations for Project State
- **project_management**: save_history method added to Project State
- **project_management**: History Model for Project State added
- **project_management**: History Model migrations for Project Milestone
- **project_management**: save_history method added to Project Milestonr
- **project_management**: History Model for Project Milestone added
- **project_management**: History Model migrations for Project
- **project_management**: save_history method added to Project
- **project_management**: History Model for Project added
- **itim**: History Model migrations for Service
- **itim**: save_history method added to Service
- **itim**: History Model for Service added
- **itim**: History Model migrations for Port
- **itim**: save_history method added to Port
- **itim**: History Model for Port added
- **itim**: History Model migrations for Cluster Type
- **itim**: save_history method added to Cluster TYpe
- **itim**: History Model for Cluster Type added
- **itim**: History Model migrations for Cluster
- **itim**: save_history method added to Cluster
- **itim**: History Model for Cluster added
- **itam**: History Model migrations for Software Version
- **itam**: save_history method added to Software Version
- **itam**: History Model for Software Version added
- **itam**: History Model migrations for Software Category
- **itam**: save_history method added to Software Category
- **itam**: History Model for Software Category added
- **itam**: History Model migrations for Software
- **itam**: save_history method added to Software
- **itam**: History Model for Software added
- **itam**: History Model migrations for Operating System Version
- **itam**: save_history method added to Operating System Version
- **itam**: History Model for Operating System Version added
- **itam**: History Model migrations for Device Type
- **itam**: save_history method added to Device Type
- **itam**: History Model for Device Type added
- **itam**: History Model migrations for Device Operating System
- **itam**: save_history method added to Device Operating System
- **itam**: History Model for Device Operating System added
- **itam**: History Model migrations for Operating System
- **itam**: save_history method added to Operating System
- **itam**: History Model migrations for Operating System
- **itam**: History Model migrations for Device Software
- **itam**: History Model for Device Software added
- **itam**: save_history method added to Device
- **itam**: History Model migrations for Device Model
- **itam**: save_history method added to Device Model
- **itam**: History Model for Device Model added
- **core**: History Model migrations for Ticket Comment Category
- **core**: save_history method added to Ticket Comment Category
- **core**: History Model for Ticket Comment Category added
- **config_management**: Child History Models added to child model lists for config group hosts and software
- **core**: History Model migrations for Ticket Category
- **core**: save_history method added to Ticket Category
- **core**: History Model for Ticket Category added
- **core**: History Model migrations for Manufacturer
- **core**: save_history method added to Manufacturer
- **core**: History Model for Manufacturer added
- **config_management**: save_history method added to Config Group Software
- **config_management**: save_history method added to Config Group Hosts
- **config_management**: save_history method added to Config Groups
- **assistance**: save_history method added to Knowledge base
- **assistance**: save_history method added to Knowledge base category
- **config_management**: History Model migrations for Config Groupse + children
- **config_management**: History Model for Config Group Software added
- **config_management**: History Model for Config Group Hosts added
- **config_management**: History Model for Config Groups added
- **assistance**: History Model migrations for Knowledge base + children
- **assistance**: History Model for Knowledge base category added
- **assistance**: History Model for Knowledge base added
- **itam**: Add device history model
- **core**: History view to only display objects from the model being requested
- **core**: Add new history model to History Serializer
- **core**: Add new history model
- **development**: lint for un-used imports
- **development**: add pylit settings
- **core**: added new history model
- **api**: Device Software Viewset requires its own function to obtain the model view serializer
- **api**: Ticket Comment Viewset requires its own function to obtain the model view serializer
- **api**: Ticket Viewset requires its own function to obtain the model view serializer
- **api**: Always use a models `View` serializer for the response
- **core**: Add logic to ensure when organization changes, an action comment is created
- **core**: Add logic to ensure when parnet ticket changes, an action comment is created

### Fixes

- **settings**: App settings serializer fielad name does not exist
- **access**: dont use organization property within organization model
- **project_management**: Project milestone is not a child model
- **core**: Child models on delete must make model field null
- **project_management**: Project Milestone History is a primaryu model
- **core**: When a child model is deleted ensure entry is still created on parent model history
- **core**: when fetching url_kwargs for model history, make it dynamic for related field name
- **core**: Xorrect logic for determining view_action
- **core**: dynamically search for history object name
- **config_management**: Remove parent property from config groups
- **tests**: Correct Permission Import due to removing from access.models
- **project_management**: project Model serializer must inherit common serializer
- **core**: History audit objects must be a valid dict
- **api**: history app names can contain an underscore
- **core**: when saving history, use audit_model for content type
- **core**: add missing functions for fetching item url
- **project_management**: Opened by field set to read only for project task ticket
- **itim**: Opened by field set to read only for problem ticket
- **itim**: Opened by field set to read only for incident ticket
- **itim**: Opened by field set to read only for change ticket
- **assistance**: Opened by field set to read only for request ticket
- **core**: Ensure that if the parent ticket changes, that the logic caters for none
- **assistance**: Category can be empty for Project Task Ticket
- **assistance**: Category can be empty for Problem Ticket
- **assistance**: Category can be empty for Incident Ticket
- **assistance**: Category can be empty for Change Ticket
- **assistance**: Category can be empty for Request Ticket
- **core**: Ticket Action comment for category change must use category field

### Refactoring

- **core**: Update access imports to new path
- **core**: Update access imports to new path
- Update migrations imports to new path
- **config_management**: Update access imports to new path
- **api**: Update access imports to neew path
- **settings**: Update access imports to new path
- **project_management**: Update access imports to new path
- **itim**: Update access imports to new path
- **itam**: Update access imports to new path
- **core**: Update access imports to new path
- **config_management**: Update access imports to new path
- **assistance**: Update access imports to new path
- **base**: Update access imports to new path
- **api**: Update access imports to neew path
- **access**: Update access imports to neew path
- **access**: Move models to their own file
- **core**: move get_url to common serializer
- **api**: Update history url kwargs to use vals from model._meta
- **core**: superuser changed from import to triage access
- **core**: Ticket action comment logic only requires a single check

### Tests

- **settings**: History Entry checks for App Settings History
- **settings**: API Field Checks for App Settings History
- Model History not to save history on self
- **core**: Correct lookup for model history test setup
- **access**: remove test cases for Team prarent_object
- **access**: History Entry checks for Team model
- **access**: API Field Checks for Team History
- **access**: History Entry checks for Organization model
- **access**: API Field Checks for Organization History
- Fix History API checks for kb
- Fix History API checks for project milestone
- Fix History Entry checks for models
- **config_management**: History Entry checks for Config_group_hosts model
- **settings**: History Entry checks for External Link model
- **project_management**: History Entry checks for Project Type model
- **project_management**: History Entry checks for Project State model
- **project_management**: History Entry checks for Project Milestone model
- **project_management**: History Entry checks for Project model
- **itim**: History Entry checks for Service model
- **itim**: History Entry checks for Cluster Type model
- **itim**: History Entry checks for Port model
- **itim**: History Entry checks for Cluster model
- **itam**: History Entry checks for Software Version model
- **itam**: History Entry checks for Software Category model
- **itam**: History Entry checks for Software model
- **itam**: History Entry checks for Operating System Version model
- **itam**: History Entry checks for Operating System model
- **itam**: History Entry checks for Device Type model
- **itam**: History Entry checks for Device OS model
- **itam**: History Entry checks for Device Model model
- **itam**: History Entry checks for Device model
- **core**: History Entry checks for Ticket Comment Category model
- **core**: History Entry checks forTicket Category model
- **config_management**: History Entry checks for Config Groups Software model
- **config_management**: History Entry checks for Config Groups model
- **assistance**: History Entry checks for Knowledge base category model
- **assistance**: History Entry checks for Knowledge base model
- **itam**: Device Software History Entry checks
- **core**: Manufacturer History Entry checks
- **core**: Model History Entries Test Suite
- **core**: History Model Unit test cases for model and tenancy checks
- **settings**: API Field Checks for External Links History
- **project_management**: API Field Checks for Project Type History
- **project_management**: API Field Checks for Project State History
- **project_management**: API Field Checks for Project Milestone History
- **project_management**: API Field Checks for Project History
- **itim**: API Field Checks for Service History
- **itim**: API Field Checks for Port History
- **itim**: API Field Checks for Cluster Type History
- **itim**: API Field Checks for Cluster History
- **core**: API Field Checks for Ticket Comment Category History
- **core**: API Field Checks for Ticket Category History
- **config_management**: API Field Checks for Config Group Software History
- **config_management**: API Field Checks for Config Group Hosts History
- **config_management**: API Field Checks for Config Group History
- **assistance**: API Field Checks for Knowledge base category History
- **assistance**: API Field Checks for Knowledge base History
- **itam**: API Field Checks for Software Version History
- **itam**: API Field Checks for Software Category History
- **itam**: API Field Checks for Software History
- **itam**: API Field Checks for Operating System Version History
- **itam**: API Field Checks for Operating System History
- **itam**: API Field Checks for Device Type History
- **itam**: API Field Checks for Device OS History
- **itam**: API Field Checks for Device Model History
- **itam**: API Field Checks for Device History
- **core**: Unit Test Suite for History Model API field checks urls can either be str or hyperlink
- **itam**: API Field Checks for Device Software History
- **core**: API Field Checks for Manufacturer History
- **core**: API Field Checks for Model History
- **core**: Unit Test Suite for History Model API field checks
- **core**: Functional Test for History Model APIPermission updated to cater for tenancy obj
- **core**: Functional Test for History Model API Permissions and Metadata
- **core**: Unit Test for History Model Viewset
- **itam**: remove test cases for os version model.parent_object as it's not required
- **core**: disable hisotry viewset function test
- **core**: correct kwargs for history tests
- **core**: Remove old history model viewset tests
- Disable Old History Model test suites
- **core**: Ensure that when parent_ticket changes on a ticket an action comment is created
- **core**: Confirm on category change to ticket that an action comment is created

## 1.10.1 (2025-02-14)

### Fixes

- **python**: Dont use system TimeZone data, use python zoneinfo module zone data

## 1.10.0 (2025-02-10)

### feat

- **settings**: Provide user with the ability to set browser mode
- **core**: Parent Ticket validation added to ticket serializer
- **core**: Add to ticket endpoint the ability to filter using `parent_ticket`
- **core**: Add to ticket model  a function for circular dependecy check of parent ticket
- **core**: Migrate Notes data to new table
- **project_management**: Add notes tab to Project Milestone details page
- **itam**: Add notes tab to Software Version details page
- **itam**: Add notes tab to Operating System details page
- **core**: Ensure when editing a model note, the modified user is updated.
- **assistance**: Knowledge Base Category Notes viewset
- **assistance**: Knowledge Base Category Notes Serializer
- **assistance**: Knowledge Base Category Notes Model
- **project_management**: Project Type Notes ViewSet
- **project_management**: Project Type Notes Serializer
- **project_management**: Project Type Notes Model
- **project_management**: Project State Notes ViewSet
- **project_management**: Project State Notes Serializer
- **project_management**: Project State Notes Model
- **project_management**: Project Milestone Notes ViewSet
- **project_management**: Project Milestone Notes Serializer
- **project_management**: Project Milestone Notes Model
- **itam**: Software Version Notes ViewSet
- **itam**: Software Version Notes Serializer
- **itam**: Software Version Notes Model
- **itam**: Software Category Notes ViewSet
- **itam**: Software Category Notes Serializer
- **itam**: Software Category Notes Model
- **itam**: Operating System Version Notes ViewSet
- **itam**: Operating System Version Notes Serializer
- **itam**: Operating System Version Notes Model
- **settings**: External Link Notes ViewSet
- **settings**: External Link Notes Serializer
- **settings**: External Link Notes Model
- **itam**: Device Model Notes ViewSet
- **itam**: Device Model Notes Serializer
- **itam**: Device Model Notes Model
- **itam**: Device Type Notes ViewSet
- **itam**: Device Type Notes Serializer
- **itam**: Device Type Notes Model
- **core**: Create an action comment on a ticket when the category changes
- **itim**: Porte Notes ViewSet
- **itim**: Porte Notes Serializer
- **itim**: Porte Notes Model
- **itim**: Cluster Type Notes ViewSet
- **itim**: Cluster Type Notes Serializer
- **itim**: Cluster Type Notes Model
- **project_management**: Project Notes ViewSet
- **project_management**: Project Notes Serializer
- **project_management**: Project Notes Model
- **itim**: Service Notes ViewSet
- **itim**: Service Notes Serializer
- **itim**: Service Notes Model
- **itim**: Cluster Notes ViewSet
- **itim**: Cluster Notes Serializer
- **itim**: Cluster Notes Model
- **itam**: Software Notes ViewSet
- **itam**: Software Notes Serilaizer
- **itam**: Software Notes Model
- **itam**: Operating System Notes ViewSet
- **itam**: Operating System Notes Serializer
- **itam**: Operating System Notes Model
- **core**: Manufacturer Notes viewset
- **core**: Manufacturer Notes serializer
- **core**: Manufacturer Notes Model
- **config_management**: Config Group Notes ViewSet
- **config_management**: Config Group Notes Serializer
- **config_management**: Config Group Notes Model
- **assistance**: Knowledge Base Notes ViewSet
- **assistance**: Knowledge Base Notes Serializer
- **assistance**: Knowledge Base Notes Model
- **access**: Team Notes ViewSet
- **access**: Team Notes Serializer
- **access**: Team Notes Model
- **access**: Organization Notes ViewSet
- **access**: Organization Notes Serializer
- **access**: Organization Notes Model
- **itam**: Device Notes ViewSet
- **itam**: Device Notes Serializer
- **itam**: Device Notes Model
- **core**: Base viewset for model notes
- **core**: Base serializer for model notes
- **core**: Base model for model notes
- **core**: Add failsafe to throw an exception if no action comment will be created
- **core**: Add field parent_ticket to base ticket view serializer
- **project_management**: Add field parent_ticket to project task ticket view serializer
- **itim**: Add field parent_ticket to problem ticket view serializer
- **itim**: Add field parent_ticket to incident ticket view serializer
- **itim**: Add field parent_ticket to change ticket view serializer
- **assistance**: Add field parent_ticket to request ticket view serializer
- **core**: Add field parent to ticket model

### Fixes

- **core**: Dont attempt to access parent_ticket field during ticket validation if it does not exist
- **core**: Permissions require the parent model for model notes
- **access**: field organization requires team related_model for org
- **core**: Use generic APIError for ticket save when no action comment will be created

### Refactoring

- Squash migrations so there is less of them for model notes
- **access**: Dont add releationship from tenancyObject.organization to organization model

### Tests

- **settings**: Test User Settings API render to ensure browser_model exists and is the correct type
- **settings**: Test User Settings model to ensure `browser_mode` field exists
- **access**: Team Note Model Check object requires org
- **settings**: External Links Note Model Checks
- **project_management**: Project Type Note Model Checks
- **project_management**: Project State Note Model Checks
- **project_management**: Project Note Model Checks
- **project_management**: Project Milestone Note Model Checks
- **itim**: Service Note Model Checks
- **itim**: Port Note Model Checks
- **itim**: Cluster Type Note Model Checks
- **itim**: Cluster Note Model Checks
- **itam**: Software Version Note Model Checks
- **itam**: Software Note Model Checks
- **itam**: Software Category Note Model Checks
- **itam**: Operating System Version Note Model Checks
- **itam**: Operating System Note Model Checks
- **itam**: Device Type Note Model Checks
- **itam**: Device Note Model Checks
- **itam**: Device Model Note Model Checks
- **core**: Manufacturer Note Model Checks
- **config_management**: Config Group Note Model Checks
- **assistance**: KB Note Model Checks
- **assistance**: KB Category Note Model Checks
- **access**: Team Note Model Checks
- **access**: Organization Note Model Checks
- **core**: Model Notes Test Suite
- **settings**: Serializer Checks for External Links Notes
- **Project_management**: Serializer Checks for Project Type Notes
- **Project_management**: Serializer Checks for Project State Notes
- **Project_management**: Serializer Checks for Project Notes
- **Project_management**: Serializer Checks for Project Milestone Notes
- **itim**: Serializer Checks for Service Notes
- **itim**: Serializer Checks for Port Notes
- **itim**: Serializer Checks for Cluster Type Notes
- **itim**: Serializer Checks for Cluster Notes
- **itam**: Serializer Checks for Software Version Notes
- **itam**: Serializer Checks for Software Notes
- **itam**: Serializer Checks for Software Category Notes
- **itam**: Serializer Checks for Operating System Version Notes
- **itam**: Serializer Checks for Operating System Notes
- **itam**: Serializer Checks for Device Type Notes
- **itam**: Serializer Checks for Device Notes
- **itam**: Serializer Checks for Device Model Notes
- **core**: Serializer Checks for Manufacturer Notes
- **config_management**: Serializer Checks for Config Groups Notes
- **assistance**: Serializer Checks for KB Notes
- **assistance**: Serializer Checks for KB Category Notes
- **access**: Serializer Checks for Team Notes
- **access**: Serializer Checks for Organization Notes
- **core**: Test Suite for Model Notes checks
- **api**: API Fileds user to be super user for tests to run
- **settings**: External Links Notes Function Viewset Tests
- **project_management**: Project Type Notes Function Viewset Tests
- **project_management**: Project State Notes Function Viewset Tests
- **project_management**: Project Notes Function Viewset Tests
- **project_management**: Project Milestone Notes Function Viewset Tests
- **itim**: Service Notes Function Viewset Tests
- **itim**: Port Notes Function Viewset Tests
- **itim**: Cluster Types Notes Function Viewset Tests
- **itim**: Cluster Notes Function Viewset Tests
- **itam**: Software Version Notes Function Viewset Tests
- **itam**: Software Notes Function Viewset Tests
- **itam**: Software Category Notes Function Viewset Tests
- **itam**: Operating System Version Notes Function Viewset Tests
- **itam**: Operating System Notes Function Viewset Tests
- **itam**: Device Type Notes Function Viewset Tests
- **itam**: Device Notes Function Viewset Tests
- **itam**: Device Model Notes Function Viewset Tests
- **core**: Manufacturer Notes Function Viewset Tests
- **config_management**: Config Groups Notes Function Viewset Tests
- **assistance**: Knowledge Base Notes Function Viewset Tests
- **assistance**: Knowledge Base Category Notes Function Viewset Tests
- **access**: Team Notes Function Viewset Tests
- **access**: Organization Notes Function Viewset Tests
- **core**: Model Notes Test Cases
- Remove old notes model tests
- **settings**: External Notes Test Cases for ViewSet
- **project_management**: Project Type Notes Test Cases for ViewSet
- **project_management**: Project State Notes Test Cases for ViewSet
- **project_management**: Project Notes Test Cases for ViewSet
- **project_management**: Project Milestone Notes Test Cases for ViewSet
- **itim**: Service Notes Test Cases for ViewSet
- **itim**: Port Notes Test Cases for ViewSet
- **itim**: Cluster Type Notes Test Cases for ViewSet
- **itim**: Cluster Notes Test Cases for ViewSet
- **itam**: Software Version Notes Test Cases for ViewSet
- **itam**: Software Notes Test Cases for ViewSet
- **itam**: Software Category Notes Test Cases for ViewSet
- **itam**: Operating System Version Notes Test Cases for ViewSet
- **itam**: Operating_system Notes Test Cases for ViewSet
- **itam**: Device Type Notes Test Cases for ViewSet
- **itam**: Device Notes Test Cases for ViewSet
- **itam**: Device Model Notes Test Cases for ViewSet
- **core**: Manufacturer Notes Test Cases for ViewSet
- **config_management**: Config Groups Notes Test Cases for ViewSet
- **assistance**: Knowledge Base Notes Test Cases for ViewSet
- **assistance**: Knowledge Base Category Notes Test Cases for ViewSet
- **access**: Team Notes Test Cases for ViewSet
- **access**: Organization Notes Test Cases for ViewSet
- **project_management**: Correct kwargs for Project Milestone Notes Test Cases for API Field Checks
- **assistance**: Knowledge Base Category Notes Test Cases for API Field Checks
- **Settings**: External Link Notes Test Cases for API Field Checks
- **project_management**: Project Type Notes Test Cases for API Field Checks
- **project_management**: Project State Notes Test Cases for API Field Checks
- **project_management**: Project Notes Test Cases for API Field Checks
- **project_management**: Project Milestone Notes Test Cases for API Field Checks
- **itim**: Service Notes Test Cases for API Field Checks
- **itim**: Port Notes Test Cases for API Field Checks
- **itim**: Cluster Types Notes Test Cases for API Field Checks
- **itim**: Cluster Notes Test Cases for API Field Checks
- **itam**: Software Version Notes Test Cases for API Field Checks
- **itam**: Software Notes Test Cases for API Field Checks
- **itam**: Software Category Notes Test Cases for API Field Checks
- **itam**: Device Type Notes Test Cases for API Field Checks
- **itam**: Device Notes Test Cases for API Field Checks
- **itam**: Device Model Notes Test Cases for API Field Checks
- **itam**: Operating System Test Cases for API Field Checks
- **itam**: Operating System Version Test Cases for API Field Checks
- **core**: Manufacturer Test Cases for API Field Checks
- **config_management**: Config Group Test Cases for API Field Checks
- **assistance**: KB Test Cases for API Field Checks
- **access**: Team Test Cases for API Field Checks
- **access**: Organization Test Cases for API Field Checks
- **core**: Model Notes Base Test Cases for API Field Checks
- remove old notes model tests
- Update url_name to match new notes endpoint
- **config_Management**: Update url_name to match new notes endpoint
- **core**: Remove notes test cases for previous notes model

## 1.9.0 (2025-02-06)

### feat

- **core**: Validate user field to ensure ticket comments always have user who added comment
- **core**: Cache ticket linked item queryset
- Views to cache discovered serializer
- **core**: When changing ticket description create an action comment with the details
- **core**: When changing a ticket real finish date create an action comment with the details
- **core**: When changing a ticket real start date create an action comment with the details
- **core**: When changing a ticket planned finish date create an action comment with the details
- **core**: When changing a ticket planned start date create an action comment with the details
- **core**: When changing a ticket milestone create an action comment with the changed details
- **core**: Add Priority badge field to ALL ticket types
- **core**: Add Impact badge field to ALL ticket types
- **core**: Add urgency badge field to ALL ticket types

### Fixes

- **project_management**: Add missing attribute `view_description` to project tasks viewset
- **settings**: Add missing attribute `view_description` to user settings viewset
- **settings**: Add missing attribute `view_description` to app settings viewset
- **itim**: Add missing attribuite to problem ticket viewset
- **itim**: Add missing attribuite to incident ticket viewset
- **itim**: Add missing attribuite to change ticket viewset
- **itimm**: correct truthy check for service device ViewSet property when evaluating queryset
- **itam**: correct truthy check for service cluster ViewSet property when evaluating queryset
- **itam**: correct truthy check for service cluster ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for service device ViewSet property when evaluating serializer_class
- **itam**: add missing attribute view_name to celery log viewset
- **api**: correct get_view_name to prioritize view_name over model.verbose_name
- **itam**: correct truthy check for software version ViewSet property when evaluating queryset
- **itam**: correct truthy check for os version ViewSet property when evaluating queryset
- **itam**: correct truthy check for device software ViewSet property when evaluating queryset
- **itam**: correct truthy check for device os ViewSet property when evaluating queryset
- **itam**: correct truthy check for software version ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for software category ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for os version ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for device software ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for device os ViewSet property when evaluating serializer_class
- **core**: correct varname for queryset within notes queryset
- **core**: add missing attribute view_description to ticket linked item viewset
- **core**: add missing attribute view_description to ticket comment viewset
- **core**: add missing attribute view_description to note viewset
- **core**: add missing attribute view_description to related ticket log viewset
- **core**: add missing attribute view_description to celery log viewset
- **core**: add missing attribute view_description to history viewset
- **core**: correct truthy check for notes ViewSet property when evaluating serializer_class
- **core**: correct truthy check for history ViewSet property when evaluating queryset
- **core**: correct truthy check for notes ViewSet property when evaluating queryset
- **core**: correct truthy check for related ticket ViewSet property when evaluating queryset
- **core**: correct truthy check for ticket comment ViewSet property when evaluating queryset
- **core**: correct truthy check for ticket linked items ViewSet property when evaluating queryset
- **core**: correct truthy check for ticket linked items ViewSet property when evaluating queryset
- **core**: correct truthy check for ticket comment ViewSet property when evaluating queryset
- **core**: correct truthy check for related ticket ViewSet property when evaluating queryset
- **core**: correct truthy check for history ViewSet property when evaluating queryset
- **core**: correct truthy check for celery log ViewSet property when evaluating queryset
- **core**: correct truthy check for Ticket Base ViewSet property when evaluating queryset
- **core**: correct truthy check for ticket base ViewSet property when evaluating serializer_class
- **assistance**: Add missing attribute `view_description` to request ticket ViewSet
- **settinggs**: Add missing attribute `view_description` to external links ViewSet
- **core**: Add missing attribute `view_description` to ticket comment category ViewSet
- **core**: Add missing attribute `view_description` to ticekt category ViewSet
- **core**: Add missing attribute `view_description` to Manufacturer ViewSet
- **project_management**: correct truthy check for project milestone ViewSet property when evaluating queryset
- **settings**: correct truthy check for user settings ViewSet property when evaluating serializer_class
- **settings**: correct truthy check for external links ViewSet property when evaluating serializer_class
- **settings**: correct truthy check for app settings ViewSet property when evaluating serializer_class
- **project_management**: correct truthy check for project milestone ViewSet property when evaluating queryset
- **project_management**: correct truthy check for project ViewSet property when evaluating serializer_class
- **project_management**: correct truthy check for project type ViewSet property when evaluating serializer_class
- **project_management**: correct truthy check for project state ViewSet property when evaluating serializer_class
- **project_management**: correct truthy check for project milestone ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for service ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for port ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for cluster ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for cluster type ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for software ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for os ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for device ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for device type ViewSet property when evaluating serializer_class
- **itam**: correct truthy check for device model ViewSet property when evaluating serializer_class
- **core**: correct truthy check for ticket comment category ViewSet property when evaluating serializer_class
- **core**: correct truthy check for ticket category ViewSet property when evaluating serializer_class
- **core**: correct truthy check for manufacturer ViewSet property when evaluating serializer_class
- **config_management**: correct truthy check for config group ViewSet property when evaluating queryset
- **config_management**: correct truthy check for config group ViewSet property when evaluating serializer_class
- **config_management**: correct truthy check for config group software ViewSet property when evaluating serializer_class
- **config_management**: correct truthy check for config group software ViewSet property when evaluating queryset
- **assistance**: correct truthy check for model kb article ViewSet property when evaluating queryset
- **assistance**: correct truthy check for model kb article ViewSet property when evaluating serializer_class
- **assistance**: correct truthy check for kb ViewSet property when evaluating serializer_class
- **assistance**: correct truthy check for kb ViewSet property when evaluating serializer_class
- **access**: correct truthy check for team ViewSet property when evaluating serializer_class
- **access**: correct truthy check for team ViewSet property when evaluating queryset
- **access**: correct truthy check for team user ViewSet property when evaluating queryset
- **access**: correct truthy check for team user ViewSet property when evaluating serializer_class
- **access**: correct truthy check for organization ViewSet property when evaluating serializer_class
- **api**: correct truthy check for set property when evaluating serializer_class
- **api**: correct truthy check for set property when evaluating queryset
- **api**: correct variable name in common viewset for queryset
- **config_management**: config group software viewset must cache queryset
- **config_management**: config group viewset must cache queryset
- **assistance**: Knowledge base category viewset must cache serializer_class
- **access**: Team viewset must cache serializer_class
- **access**: Team viewset must cach queryset
- **access**: Team User viewset must cach queryset
- **api**: Add missing property `bacjk_url` to Common viewset
- **api**: Common viewset to cache and use queryset Object
- **access**: When conduting permission check for user settings, if user not owner of settings, deny access
- **access**: when checking object permissions, dont cast obj to int untill checking it exists
- **access**: org mixin get_obj_org not to call get_object
- **core**: ensure item_type exists before trying to get queryset
- **core**: Ticket Action comment date fields must be checked if empty before use
- **settings**: grant the user access to their own settings object
- **settings**: grant the user access to their own settings

### Refactoring

- **access**: when checking obj permission use view cached obj organization
- **access**: When fetching obj org, if pk exist attempt to fetch object
- **core**: When fetching a ticket, fetch related fields
- **core**: Ticket action comment for changing milestone to use item tasg
- **core**: Ticket action comment for changing project to use item tasg

### Tests

- **core**: Add missing unit tests for notes ticket viewset
- **settings**: Add missing unit tests for user settings ticket viewset
- **settings**: Add missing unit tests for app settings ticket viewset
- **project_management**: Add missing unit tests for project task ticket viewset
- **api**: Add kwargs as arg to test cases
- **itim**: Add missing unit tests for problem ticket viewset
- **itim**: Add missing unit tests for incident ticket viewset
- **itim**: Add missing unit tests for change ticket viewset
- **core**: add permisssion class override test case for celery results
- Add empty kwargs to ViewSet index page test cases
- **itam**: Add missing unit tests for software version viewset
- **itam**: Add missing unit tests for software categories viewset
- **itam**: Add missing unit tests for os versions viewset
- **itam**: Add missing unit tests for software installs viewset
- **itam**: Add missing unit tests for os installs viewset
- **itam**: Add missing unit tests for device software viewset
- **itam**: Add missing unit tests for device operating system viewset
- **api**: Add kwargs as arg to test cases
- **core**: Add missing unit tests for ticket linked items viewset
- **core**: Add missing unit tests for ticket comment viewset
- **core**: Add missing unit tests for celery log viewset
- **core**: Add missing unit tests for history viewset
- **core**: Add missing unit tests for related tickets viewset
- **assistance**: Add missing unit tests for request ticket viewset
- **api**: queryset and serializer_class test cases updated to use Fake request object
- **settings**: Add missing unit tests for external links viewset
- **project_management**: Add missing unit tests for project type viewset
- **project_management**: Add missing unit tests for project state viewset
- **project_management**: Add missing unit tests for project milestone viewset
- **project_management**: Add missing unit tests for project viewset
- **itim**: Add missing unit tests for service viewset
- **itim**: Add missing unit tests for ports viewset
- **itim**: Add missing unit tests for cluster types viewset
- **itim**: Add missing unit tests for cluster viewset
- **itam**: Add missing unit tests for Software viewset
- **itam**: Add missing unit tests for Operating System viewset
- **itam**: Add missing unit tests for Device Type viewset
- **itam**: Add missing unit tests for Device Model viewset
- **itam**: Add missing unit tests for Device viewset
- **api**: dont mock the qs bool
- **core**: Add missing unit tests for Ticket Comment Category viewset
- **core**: Add missing unit tests for Ticket Category viewset
- **core**: Add missing unit tests for manufacturer viewset
- **config_management**: Add missing unit tests for config groups software viewset
- **config_management**: Add missing unit tests for config groups viewset
- **assistance**: Add missing unit tests for Model Knowledge Base Article viewset
- **assistance**: Add missing unit tests for Knowledge Base Category viewset
- **assistance**: Add missing unit tests for Knowledge Base viewset
- **access**: Add missing unit tests for team user viewset
- **access**: Add missing unit tests for team viewset
- **access**: Add missing unit tests for organization viewset
- **base**: Ensure viewsets are caching and using the serializer_class object
- **base**: Ensure viewsets are caching and using the queryset object
- **core**: Test case to ensure ticket comment always has user added
- **settings**: when checking if user can delete own settings, user must be owner of settings
- **settings**: regardless of permissions a user can change their own settings
- **access**: during permission check function has_permission ensure `get_object` not called
- **core**: Ensure that an action comment is created when ticket description is edited
- **core**: Ticket Action comment test cases for real_finish_date actions
- **core**: Ticket Action comment test cases for real_start_date actions
- **core**: Ticket Action comment test cases for planned_finish_date actions
- **core**: Ticket Action comment test cases for planned_start_date actions
- **core**: Ticket Action comment test cases for milestone actions
- **core**: Ticket Action comment test cases for project actions
- **core**: Ticket Action comment tests moved to their own suite
- **core**: Unit test cases for ticket urgency_badge field checks
- **core**: Unit test cases for ticket priority_badge field checks
- **core**: Unit test cases for ticket impact_badge field checks
- **settings**: Remove no-permission failure test as user settings require no permissions

## 1.8.0 (2025-01-23)

### feat

- **python**: update django 5.1.4 -> 5.1.5
- **access**: TenancyManager object to cache the users team lokkup
- **access**: if organization object casted to int, return organization.id
- **base**: Dont enable metrics by default
- **base**: Add exporter to celery
- **base**: Add exporter to gunicorn
- **base**: Add django-prometheus for metrics export
- **api**: fetch doc path for view metadata
- **settings**: Add new field button text
- **itim**: Ability to add external link to a service
- **access**: Add organization to team display_name
- **assistance**: add category and org to model articles tab
- **api**: Enable fetching related ticket metadata for the other side of the related ticket
- **core**: Add ticket comment field metadata to api meta
- **core**: Add ticket linked item field metadata to api meta
- **core**: Add related ticket field metadata to api meta
- **api**: Add option to viewset to render field markdown metadata
- **api**: Add item metadata to markdown field for renderable items
- **api**: Add item metadata to markdown field for renderable items

### Fixes

- **core**: triage user requires access to date fields for change, incident, problem and project task tickets
- **core**: triage user requires access to date fields for tickets
- **core**: User must be a required field for ticket comment
- **access**: use request object passed to has_object_permission
- **core**: ensure when updating, reques.tenancy object perm checking is used
- **project**: when creating a project, fetch the organization object
- **api**: Only attempt to access a app_settings object for org field if request object exists
- **core**: When adding a ticket, query for org
- **access**: use the request user teams within Manager
- **access**: cached orgs is an int list
- **base**: metrics dir env var PROMETHEUS_MULTIPROC_DIR must ALWAYS exist
- **base**: Dynammic settings determined by if metrics are enabled
- **access**: Return API exception, not django
- **api**: correctly return API exceptions for user to rectify
- **core**: Set user whom added comment as comment user
- **core**: display_name is not a mandatory field for related ticket
- **core**: display_name is not a mandatory field for ticket linked item
- **api**: Ensure ALL required classes for viewset are inherited

### Refactoring

- **access**: Dont override django middleware, create own for access tenancy
- **access**: Move user perm logic to request.tenancy object
- Move app_settings object to request object
- **access**: cache app settings during perm check
- **access**: prefetch team related fields

### Tests

- **core**: Correct ticket tests as triage user is supposed to  have access to ticket date fields
- update to cater for tenancy object in request
- Initial k6s individual page speed test cases
- **app**: metrics_enabled setings checks
- **app**: refactor. order tests alphanumerical
- **api**: ensure documentation key and data is added to API metadata
- **settings**: check to ensure API fields returned are present and correct type for external_links model
- **assistance**: Ensure category fields are present for model articles

## 1.7.0 (2025-01-04)

### feat

- **access**: Enable Objects from global organization to be viewable by user with the permission
- **access**: Enable Objects from globally set organization to return within query
- **access**: Enable the calling of the dynamic permissions function to obtain permissions
- **itam**: Cater for RabbitMQ errors when uploading inventory
- **itam**: On Inventory upload validate existing device
- **access**: During permission checking also capture Http404
- **access**: Super User to be granted permission
- **access**: Cache the permission required during permission checking
- **api**: Add `IndexViewset` to ViewSet mixin
- **access**: If the user lacks the permission during permission checks, return sooner
- **access**: Enforce view action and HTTP/Method match for permission checks
- **itim**: External Links to display on cluster details page
- **api**: Add API v2 Endpoint for cluster services
- **api**: distinguish between read-only and authenticateed user permissions

### Fixes

- **api**: Ensure ALL required classes for viewset are inherited
- **itam**: Dont query parent class for permissions
- **core**: If no org specified serializer fetch, dont attempt to access
- **access**: If no org specified during permission check, rtn false for permission
- **itam**: return serializer for inventory endpoint
- **api**: base index must inherit from IndexViewset
- **core**: Dont attempt to access the object if it doesn't exist when fetching ticket permissions
- **access**: Cached list objects must be a list including an empty one as required
- **core**: when gather ticket permissions, use getter as object may not exist
- **core**: action metadata to use view permission for tickets
- **access**: Use request.method for determining the HTTP/Method for permission checks
- **access**: Add HTTP/Method=DELETE as valid option  for object delete/destroy.
- **access**: Ensure Object permission are checked when an object is having an action performed against it.
- **core**: History View is a read-only view
- **core**: Permissions for Related ticket to be derived from ticket org
- **access**: Team User permission organiztion is team org

### Refactoring

- **itam**: Device UUID field requires no default
- **itam**: mv inventory task to itam app
- **access**: Use exceptions for permission flow as required
- **api**: dedup code within viewset mixin
- **access**: Object permission checking moved to `has_object_permission` function
- **access**: move ability to get required permissions from permissions mixin to organization mixin
- **core**: move ticket linked item to dynamic parent model
- **api**: Use new re-writen Mixins for Tenancy and Permission checks
- **access**: Organization Permission Mixin now caters for API ONLY
- **access**: Organization Mixin now caters for API ONLY

### Tests

- **access**: Skip test case for appsettings different organization due to model not being tenancy model.
- **access**: Ensure items returned from query are from user organization and/or globally set organization
- **itam**: API v2 Inventory Permission Check skip diff org
- **itam**: API v2 Inventory Permission Checks
- mv inventory test to itam app
- **access**: Test Cases for Organization Permission Mixin
- **api**: Adjust test case for metadata visibility
- **core**: remove different org testcase from history checks
- **core**: When testing if history access is possible for user with perms, correct status is HTTP/200
- **access**: When adding org, test case must use non-super user
- **itim**: Ensure external_links are returned as part of _urls
- **itim**: Add API v2 permission checks for cluster services
- **itim**: Add API v2 permission checks for device services

## 1.6.0 (2024-12-23)

### feat

- **access**: Check if organization field is read-only during permission check
- **access**: Ability to specify parent model for permission to do
- **information_management**: add cluster type kb article linking
- **information_management**: Ability to link Knowledge Base article to a Software
- **information_management**: Ability to link Knowledge Base article to a Software
- **information_management**: Ability to link Knowledge Base article to a Software Category
- **information_management**: Ability to link Knowledge Base article to a Operating System Version
- **information_management**: Ability to link Knowledge Base article to a Operating System
- **information_management**: Ability to link Knowledge Base article to a Device
- **information_management**: Ability to link Knowledge Base article to a Device Type
- **information_management**: Ability to link Knowledge Base article to a Device Model
- **information_management**: Ability to link Knowledge Base article to an External Link
- **information_management**: Ability to link Knowledge Base article to a Project
- **information_management**: Ability to link Knowledge Base article to a Project Type
- **information_management**: Ability to link Knowledge Base article to a Project State
- **information_management**: Ability to link Knowledge Base article to a Project Milestone
- **information_management**: Ability to link Knowledge Base article to a Service
- **information_management**: Ability to link Knowledge Base article to a Port
- **information_management**: Ability to link Knowledge Base article to a Cluster Type
- **information_management**: Ability to link Knowledge Base article to a Cluster
- **information_management**: Ability to link Knowledge Base article to a Ticket Category
- **information_management**: Ability to link Knowledge Base article to a Manufacturer
- **information_management**: Ability to link Knowledge Base article to a Config Group
- **information_management**: Ability to link Knowledge Base article to a Team
- **information_management**: Ability to link Knowledge Base article to an Organization
- **information_management**: Add API v2 Endpoint for model KB articles
- **information_management**: Add method `get_url` to model kb article
- **information_management**: DB Model for linking KB articles to models
- **assistanace**: remove kb article content from details tab
- **core**: call models `clean` method prior to saving model to DB
- **api**: during permission checking, if model is an organization and the user is a manager allow access to the organization.
- **api**: If user is organization manager of any org, show organization within navigation
- **core**: Link Team to ticket
- **core**: Link Organization to ticket
- **core**: Link KB to ticket
- **access**: Add project_management permissions to teams avail permissions

### Fixes

- **core**: Add missing KB article delete signal for ticket linking cleanup
- **core**: Ensure for KB article permissions can be correctly checked
- **core**: use cooorect model name for choices
- **itam**: Use Device organization for device operating system
- **settings**: remove field `owner_organization` from App Settings
- **core**: Use object organization for ticket linked items
- **itam**: Use Software organization for Software Version
- **itam**: Use Operating System organization for OS Version
- **itam**: Use Device organization for device software
- **core**: Use Ticket organization for ticket linked items
- **core**: Use parent model organization for object notes
- **access**: During permission checking also use `get_serializer` if avail
- **access**: default to empty when attempting to get view attribute
- **core**: Use ticket organization for permission checking for adding a comment
- **itam**: KB url must use `obj` not `item` when building ursl for device type
- **itam**: KB url must use `obj` not `item` when building ursl for device model
- **core**: Add missing migrations for linking kb to ticket
- **core**: Ensure that a user cant reply to a discussion reply
- **core**: Add Org, Team and KB article to ticket linked Item serializer
- **core**: Ticket Linked Item serializer removed from inheriting from common serializer.
- **core**: Ticket model serializer must inherit from common serializer
- **core**: Ticket Related Item model serializer must inherit from common serializer
- **core**: Ticket Linked Item model serializer must inherit from common serializer
- **core**: Ticket Comment  model serializer must inherit from common serializer
- **core**: Notes model serializer must inherit from common serializer
- **docker**: Correct nginx proxy headers passed to gunicorn
- **core**: Generate the correct url for a ticket comment when it's a discussion
- **core**: organization field set to `write_only=True`
- **core**: If ticket comment is a reply, add the parent id post validation

### Refactoring

- **access**: Adjust permission check logic to use try..catch instead of gettattr due to base method throwing exception
- **base**: move model calling of clean to tenancy model class
- **docker**: gunicorn config moved to con file
- **core**: Add ticket comment organization post validation

### Tests

- **core**: KB article delete ticket link clean up checks
- **core**: KB Ticket linking serializer checks
- **core**: KB Ticket linking permission checks
- **core**: Add data for ticket comment does not use organization field
- revert test case changes from 1c065601f6030aeb6065fa9f1b9afb23e1783646
- **information_management**: Add model test cases for Model KB Article
- **information_management**: Add API v2 Endpoint test cases for Model KB Article
- **information_management**: Add Viewset test cases for Model KB Article
- **information_management**: Add Serializer test cases for Model KB Article
- **api**: mv test case change denied delete to apipermissionchange test cases
- **base**: Ensure Models inherit from Tenancy and SaveHistory Classes
- **core**: test to ensure that a user cant reply to a comment that is already part of a discussion
- **core**: test to ensure that a user can reply to a comment (start comment)

## 1.5.0 (2024-12-09)

### feat

- **python**: update django 5.1.2 -> 5.1.4
- **api**: If global organization defined, filter from ALL organization fields
- **api**: Add nav menu permission checks for settings
- **api**: When fething an items url dueing metadata creation, used named parameters
- **access**: Modify Admin User panel by removing perms and adding teams
- **access**: filter permissions available
- **api**: Filter navigation menu by user permissions
- **api**: Add API version details to the metadata
- **access**: add `back` and `return_url` urls to team user metadata
- **access**: add `back` and `return_url` urls to team metadata
- **api**: Add `back` url to metadata
- **api**: Add `return_url` to metadata

### Fixes

- **settings**: Add missing `get_url` function to user_settings model
- **settings**: Add missing `get_url` function to app_settings model
- **core**: correctr the required parameters for related ticket serializer when fetching own url
- **core**: Remove requirement that ticket be specified for related tickets `get_url`
- **access**: Add missing `table_fields` attribute to team users model
- **api**: during metadata navigation permission checks, cater for non-existant keys
- **core**: Remove superfluous check from ticket viewset
- **access**: Team permissions is not a required field
- **core**: History query must also be for self, not just children
- **access**: correct team users table to correct data key

### Refactoring

- **access**: Settings must be an available permissions when setting team permissions
- **itam**: set deviceoperatingsystem model, device field to be type `onetoone`
- **assistance**: make content the first tab for kb articles
- **api**: move metadata url_return -> urls.self

### Tests

- **api**: Nav menu permission checks for settings
- **api**: Nav menu permission checks
- **core**: Correct `url.self`checks to use list view
- **core**: Dont test History for table view
- **settings**: Dont test user settings for table view
- **steeings**: Dont test app settings for table view
- **core**: Dont test related ticket for table or detail view
- **api**: Refactor test so that endpoints not expected to have an endpoint or be rendered in a table wont be tested for it.
- **settings**: API Metadata checks for user settings
- **settings**: API Metadata checks for external links
- **settings**: API Metadata checks for app settings
- **project_management**: API Metadata checks for project type
- **project_management**: API Metadata checks for project task
- **project_management**: API Metadata checks for project state
- **project_management**: API Metadata checks for project milestone
- **project_management**: API Metadata checks for project
- **itim**: API Metadata checks for problem ticket
- **itim**: API Metadata checks for incident ticket
- **itim**: API Metadata checks for change ticket
- **itim**: API Metadata checks for service
- **itim**: API Metadata checks for port
- **itim**: API Metadata checks for cluster type
- **itim**: API Metadata checks for cluster
- **itam**: API Metadata checks for software version
- **itam**: API Metadata checks for software category
- **itam**: API Metadata checks for software
- **itam**: API Metadata checks for operating system version
- **itam**: API Metadata checks for operating system
- **itam**: API Metadata checks for software
- **itam**: API Metadata checks for operating system
- **itam**: API Metadata checks for device type
- **itam**: API Metadata checks for device OS
- **itam**: API Metadata checks for device model
- **itam**: API Metadata checks for device
- **core**: API Metadata checks for ticket comment category
- **core**: API Metadata checks for ticket comment
- **core**: API Metadata checks for ticket category
- **core**: API Metadata checks for history
- **core**: API Metadata checks for related tickets
- **core**: API Metadata checks for manufacturers
- **config_management**: API Metadata checks for config group software
- **config_management**: API Metadata checks for config groups
- **access**: API Metadata checks for request ticket
- **access**: API Metadata checks for kb category
- **access**: API Metadata checks for kb
- **api**: correct metadata testcases
- **access**: API Metadata checks for organization
- **api**: API Metadata test cases for navigation menu rendering
- **api**: correct logic for test class attribute fetching
- **access**: API Metadata checks for Team User model
- **access**: API Metadata checks for Team model
- **api**: API Metadata functional Test Cases

## 1.4.1 (2024-11-30)

### Fixes

- **itam**: When validating device config, only do so if there is config defined

## 1.4.0 (2024-11-28)

### feat

- **project_management**: add project completed field
- **api**: Implement Sanity error handling for uncaught exceptions
- **itam**: Split device software serializer to include seperate software installs serializer
- **itam**: Add Operating System Installs API v2 endpoint
- **itam**: based off of the request kwaargs, adjust device serializer fields accordingly
- **itam**: Add Software installs endpoint
- **itim**: add cluster and device to Services in new UI
- **config_management**: add hosts to new UI
- **api**: add ticket icons
- **itim**: Add nodes and devices to detail view
- **api**: return_url to default to list view
- **base**: move setting `SECURE_SSL_REDIRECT = True` to etc/settings
- **base**: use senisible settings for SSL
- **itam**: Add device operating system API v2 endpoint
- **api**: Add return URL to metadata if model has attribute `get_url`
- **config_management**: Add field child group count to table fields for groups
- **itam**: Add `page_layout` to SoftwareVersion model
- **itam**: Add `page_layout` to OperatingSystemVersion model
- **project_management**: Add `page_layout` to Milestone model
- **settings**: Add `page_layout` to AppSettings model
- **access**: render team_name field as anchor
- **api**: Support setting char field as an anchor field using .urls._self
- **api**: Added abilty to specify a css class for markdown field
- Add timezone support
- **api**: Add a Common Model serializer to be inherited by all model serializers
- **core**: new field type markdown
- **core**: new field type char
- **core**: add RElated Items choices to metadata
- **itam**: Add Inventory API v2 endpoint
- **api**: Depreciate API V1 endpoint /api/config
- **core**: New signal for cleaning linked ticket items when the item is deleted
- **core**: Show milestone using base serializer for all ticket types
- **core**: Show project using base serializer for all ticket types
- **core**: Add Parse error to exceptions
- **core**: Ticket serializer to ensure user who opens ticket is subscribed to it
- **core**: Ticket serializer to validate milestone
- **core**: Ticket serializer to validate organization
- **itim**: Add Project Task API v2 endpoint
- **itim**: Add Problem Ticket API v2 endpoint
- **itim**: Add Incident Ticket API v2 endpoint
- **itim**: Add Change Ticket API v2 endpoint
- **api**: Depreciate v1 API Endpoint Assistance
- **api**: Depreciate v1 API Endpoint Request Ticket
- **api**: Depreciate v1 API Endpoint Assistance
- **api**: Depreciate v1 API Endpoint Ticket Comments
- **api**: Depreciate v1 API Endpoint Ticket Comment Categories
- **api**: Depreciate v1 API Endpoint Ticket Categories
- **core**: Ensure Related Tickets validate against duplicate entries
- **core**: Add MethodNot Allowed to Centurion exceptions
- **core**: Determine serializer from action and user permissions for Ticket Comments
- **core**: Add custom exception class
- **core**: Ensure ticket comment Serializer validates for existance of comment_type and ticket id
- **core**: Ensure ticket comment Serializer is picked based off of comment_type
- **core**: Ensure that ticket linked item validates if ticket supplied
- **core**: Ensure that ticket comment category cant assign self as parent
- **core**: Ensure that ticket category cant assign self as parent
- **core**: Add Ticket Comment Category API v2 endpoint
- **core**: Add Item Ticket API v2 endpoint
- **core**: Add Related Ticket API v2 endpoint
- **core**: Add Ticket Linked Item API v2 endpoint
- **core**: Add url function to Ticket Linked Items model
- **itim**: Add url function to Service model
- **itim**: Add url function to Cluster model
- **itam**: Add url function to Software model
- **itam**: Add url function to Operating System model
- **itam**: Add url function to Device model
- **config_management**: Add url function to Config Groups model
- **core**: Add Ticket Comment API v2 endpoint
- **core**: Add Ticket Category API v2 endpoint
- **assistance**: Add Request Ticket API v2 endpoint
- **api**: Custom exception UnknownTicketType
- **core**: Add Base Ticket Serializer and ViewSet
- **api**: Setup API to be correctly versioned
- **settings**: Add get_organization function to app settings model
- **settings**: Add Celery Task Logs API v2 endpoint
- **api**: Added ability to specify table fields within the viewset.
- **settings**: Add User Settings API v2 endpoint
- **settings**: Add App Settings API v2 endpoint
- **project_management**: Add remaining Project base serializers for API v2
- **project_management**: Project Validation for API v2
- **project_management**: Add Project Type API v2 endpoint
- **project_management**: Add Project State API v2 endpoint
- **project_management**: Add Project Milestone API v2 endpoint
- **project_management**: Add Project API v2 endpoint
- **itim**: Port Serializer Validations
- **itim**: Service Serializer Validations
- **itim**: Ensure cluster cant assign itself as parent on api v2 endpoint
- **itim**: Add Port API v2 endpoint
- **itim**: Add Cluster API v2 endpoint
- **itim**: Add Cluster Type API v2 endpoint
- **itim**: Add Service API v2 endpoint
- **itam**: Depreciate API v1 Software Endpoint
- **core**: Add Operating System Version API v2 endpoint
- **core**: Add Operating System API v2 endpoint
- **core**: Add External Link API v2 endpoint
- **itam**: Add Device Software API v2 endpoint
- **itam**: Add Device API v2 endpoint
- **itam**: Add Device Type API v2 endpoint
- **itam**: Add Software Version API v2 endpoint
- **itam**: Depreciate API v1 device endpoint
- **itam**: Add Software API v2 endpoint
- **itam**: Add Device Model API v2 endpoint
- **itam**: Add Device API v2 endpoint
- **itim**: Add Service Notes API v2 endpoint
- **core**: Add Software Notes API v2 endpoint
- **core**: Add Manufacturer API v2 endpoint
- **itim**: Add Service base serializer
- **itam**: Add operating system Base Serializer
- **config_management**: Add Notes API v2 endpoint
- **config_management**: Add History API v2 endpoint
- **config_management**: Depreciate API v1 config endpoint
- **config_management**: Add config groups to config api endpoint
- **config_management**: Add Device Base Serializer
- **itam**: Add Software Version Base Serializer
- **itam**: Add Software Base Serializer
- **config_management**: Add Config Group Software API v2 endpoint
- **config_management**: Add Config Group API v2 endpoint
- **assistance**: Ensure Knowledge Base Category cant assign self as parent category
- **assistance**: Knowledge Base Serializer Validation method added
- **assistance**: Add Knowledge Base Category API v2 endpoint
- **assistance**: Add Knowledge Base API v2 endpoint
- **api**: Depreciate API v1 permission endpoint
- **access**: Add Team Users API endpoint
- **access**: Depreciate Team API v1 endpoint
- **access**: Depreciate Organization API v1 endpoint
- **access**: Add Organization API endpoint
- **base**: Add Team API endpoint
- **base**: Add Permission API endpoint
- **base**: Add Content Type API endpoint
- **api**: Add Read Only abstract ViewSet
- **base**: Add user API endpoint
- **api**: add v2 endpoint
- **project_management**: Add attribute table_fields to Project Type model
- **project_management**: Add attribute page_layout to Project Type model
- **project_management**: Add attribute table_fields to Project State model
- **project_management**: Add attribute page_layout to Project State model
- **project_management**: Add attribute page_layout to Project Milestone model
- **project_management**: Add attribute table_fields to Project Milestone model
- **project_management**: Add attribute table_fields to Project model
- **project_management**: Add attribute page_layout to Project model
- **itim**: Add attribute table_fields to Service model
- **itim**: Add attribute page_layout to Service model
- **itim**: Add attribute table_fields to Service Port model
- **itim**: Add attribute page_layout to Service Port model
- **itim**: Add attribute table_fields to Cluster Type model
- **itim**: Add attribute page_layout to Cluster Type model
- **itim**: Add attribute table_field to Cluster model
- **itim**: Add attribute page_layout to Cluster model
- **itam**: Add attribute table_field to Software Category model
- **itam**: Add attribute table_fields to Software model
- **itam**: Add attribute page_layout to Software model
- **itam**: Add attribute table_fields to Operating System Version model
- **itam**: Add attribute page_layout to Operating System Version model
- **itam**: Add attribute table_field to Operating System model
- **itam**: Add attribute page_layout to Operating System model
- **itam**: Add attribute table_fields to "Device Type" model
- **itam**: Add attribute page_layout to "Device Type" model
- **itam**: Add attribute page_layout to "Device Software" model
- **itam**: Add attribute table_fields to "Device Software" model
- **itam**: Add attribute page_layout to "Device Software" model
- **core**: Add attribute table_fields to Ticket Comment Category model
- **core**: Add attribute page_layout to Ticket Comment Category model
- **core**: Add attribute page_layout to Ticket comment model
- **core**: Add attribute table_fields to Ticket Category model
- **core**: Add attribute page_layout to Ticket Category model
- **core**: Add attribute page_layout to Ticket model
- **core**: Add attribute page_layout to Notes model
- **core**: Add attribute table_fields to Manufacturer model
- **core**: Add attribute page_layout to Manufacturer model
- **access**: Add attribute table_fields to Config Group Software model
- **access**: Add attribute page_layout to Config Group Software model
- **access**: Add attribute table_fields to Config Groups model
- **access**: Add attribute page_layout to Config Groups model
- **access**: Add attribute table_fields to KB model
- **access**: Add attribute page_layout to KB model
- **access**: Add attribute table_fields to KB Category model
- **access**: Add attribute page_layout to KB Category model
- **access**: Add attribute table_fields to Team model
- **access**: Add attribute page_layout to Team model
- **core**: Add `table_fields` to Ticket Model
- **itam**: Add v2 endpoint ITAM
- **base**: Add User Serializer
- **settings**: Add v2 endpoint Settings
- **project_management**: Add v2 endpoint Project Management
- **itim**: Add v2 endpoint ITIM
- **config_management**: Add v2 endpoint Config Management
- **assistance**: Add v2 endpoint Assistance
- **access**: Add v2 endpoint Access
- **itim**: Add `table_fields` to Service Model
- **core**: Add `table_fields` to Device Software Model
- **core**: Add `table_fields` to Notes Model
- **core**: Add `table_fields` to History Model
- **itam**: Add `table_fields` and `page_layout` to Device Model
- **itam**: Add `table_fields` and `page_layout` to Device Model
- **core**: Add `table_fields` to Ticket Linked Item
- **core**: Add `table_fields` to Ticket Comment
- **core**: Add `table_fields` to Ticket
- **core**: Add attribute `staatus_badge` to ticket model
- **access**: Add `table_fields` and `page_layout` to Organization
- **api**: Add React UI metadata class
- **api**: Add API v2 Endpoint
- **api**: add API login template to use current login form
- **api**: Update API template to use name Centurion
- **itam**: Add category property to device software model
- **itam**: Add action badge property to device software model
- **itam**: Add status badge property to device model
- **core**: Add a icon serializer field.
- **core**: Add a badge serializer field.
- **api**: Add common ViewSet class for inheritence
- Add dependency django-cors-headers

### Fixes

- **project_management**: Correct All tickets query for calculating project completion
- **core**: Prevent a ticket from being related to itself
- **core**: when fetching ticket serializer set org=None
- **core**: use the view pk to filter self out for ticket category update
- **core**: Ensure for update of ticket the correct serializer is selected
- **core**: dont exclude self for ticket comment category if not exists
- **itam**: Add Operating System API v2 field typo
- **core**: Enusure project_task serializer sets the project_id
- **itam**: device os serializer not to show org and device
- **core**: ticket comment to use model serializer for meta
- **core**: add kwargs to notes
- **core**: correct get_url function notes
- **core**: add missing dep to notes
- **access**: correct team users get_url
- **access**: correct team get_url requires kwargs
- **core**: correct notes get_url
- **access**: correct team get_url
- **core**: ticket model url requires kwargs
- **core**: ticket comment model url requires kwargs
- **core**: dont attempt to fetch org for ticket comment if no data supplied
- **core**: Always set the organization to the ticket org when adding a ticket comment when org not specified.
- **api**: Ensure queryset filters to actual item if pk is defined
- **core**: Automagic fetch data for fields and only require ticket id to link item to ticket
- **core**: Always set the organization to the ticket org when adding a ticket comment.
- **config_management**: show parent groups only on index
- **core**: Set notes _self url to empty val then attempt to sset
- **core**: Ensure API v1 Ticket sets the ticket type prior to validation
- **core**: Dont attempt to use ticket instance organization if it's a new ticket being created
- **access**: Ensure organization is a mandatory field
- **core**: Ensure ticket and comment bodies are set to required
- **core**: correct navigation metadata
- **task**: Ensure if inventory RX is a string, serialize it
- **access**: Team User serializer not to capture exceptions
- **access**: Team User team and user fields required when creating, don't use default value.
- **access**: Team name required when creating, don't use default value.
- **access**: Dont capture exceptions within team serializer
- **core**: Ensure import user can set field `opened_by` when importing tickets
- **core**: Correct duration slash command regex
- **core**: When an item that may be linked to a ticket is deleted, remove the ticket link
- **core**: Related ticket slash command requires model to be imported
- **core**: correct missing or incomplete ticket model fields
- **core**: When creating a ticket, by default give it a status of new
- **core**: Ensure that when creating a ticket an organization is specified
- **core**: Correct Ticket read-only fields
- **core**: Correct inheritence order for ticket serializers
- **core**: Ensure Organization can be set when creating a ticket
- **core**: Ensure that when fetching ticket permission, spaces are replaced with '_'
- **core**: Ticket serializer org validator to access correct data
- **core**: Add project URL to all Ticket Types
- **core**: Add Ticket Category URL to all Ticket Types
- **core**: When obtaining ticket type use it's enum value
- **core**: Ensure triage and import permissions are catered for Tickets
- **core**: Ensure Ticket Linked Item slash command works for ticket comments
- **core**: Only use Import Serializer on Ticket Comment Create if user has perms
- **core**: Ensure related ticket slash command works for ticket comments
- **api**: Ensure `METHOD_NOT_ALLOWED` exception is thrown
- **core**: Correct serializer item field to be for view serializer ONLY
- **config_management**: Correct ticket url in group serializer
- **core**: Add missing ticket comment category url
- **core**: Add missing permissions function to ticket viewset
- **core**: Ensure that when checking linked ticket class name, spaces are replaced
- **core**: Ensure item tickets class can have underscore in name
- Dont attempt to access request within serializers when no context is present
- **core**: Add Ticket Category API v2 endpoint to urls
- **core**: Correct ticket comment model name
- **api**: Ensure read-only fields have choices added to metadata
- **api**: Correct inheritance order for ModelViewSet
- **settings**: Populate user_settings Meta
- **settings**: Populate app_settings Meta
- **project_management**: For Project use a separate Import Serializer
- **project_management**: use the post data dict for fetching edit organisation
- **project_management**: use the post data or existing object for fetching edit organisation
- **project_management**: Dont use init to adjust read_only_fields for project
- **project_management**: if user not hav org specified dont attempt to access
- **project_management**: for project serializer (api v1) ensure org is id
- **itim**: Ensure service config from template is not gathered if not defined
- **itim**: Ensure params passed to super when validating cluster
- **itim**: Correct Device Service API v2 endpoint
- **itam**: Don't attempt to include manufacturer in name for Device Model if not defined
- **itam**: Ensure software version model has page_layout field
- **core**: notes field must be mandatory
- **core**: Add missing attributes name to history model
- **config_management**: ensure validation uses software.id for config group software serializer
- **config_management**: Config Groups Serializer Validation checks
- **assistance**: Correct Knowledge Base Category serializer Validation
- **itam**: Correct inventory validation response data
- **itam**: Correct inventory api upload to use API exceptions instead of django base
- **assistance**: Add missing fields `display_name` and `model_notes` to Knowledge Base Category serializer
- **assistance**: correct KB category serializer validation
- **assistance**: Correct Knowledge Base serialaizer Validation
- **api**: on permission check error, return authorized=false
- **access**: Add missing parameters to Team User fields
- **api**: Add missing organization url routes
- **access**: ensure org id is an integer during permission checks
- **access**: if permission_required attribute doesn't exist during permission check, return empty list
- Ensure all Model fields are created with attributes `help_text` and `verbose_name`
- **api**: correct logic for permission check to use either queryset or get_queryset
- **settings**: Add attribute table_fields to External Links model
- **settings**: Add attribute page_layout to External Links model
- **settings**: Add missing attribute Meta.verbose_name to External Links model
- **settingns**: Add missing attribute Meta.ordering to External Links model
- **itam**: Add missing attribute Meta.verbose_name to Software Category model
- **itam**: Add missing attribute Meta.ordering to Software Category model
- **itam**: Add missing attribute Meta.verbose_name to Software model
- **itam**: Add missing attribute Meta.ordering to Software model
- **itam**: Add missing attribute Meta.verbose_name to Operating System Version model
- **itam**: Add missing attribute Meta.ordering to Operating System Version model
- **itam**: Add missing attribute Meta.verbose_name to Operating System model
- **itam**: Add missing attribute Meta.ordering to Operating System model
- **itam**: Add missing attribute Meta.verbose_name to "Device Type" model
- **itam**: Add missing attribute Meta.ordering to "Device Software" model
- **itam**: Add missing attribute Meta.verbose_name to "Device Software" model
- **itam**: Add missing attribute Meta.verbose_name to "Device Software" model
- **itam**: Add missing attribute Meta.ordering to "Device Software" model
- **itama**: Add missing attribute Meta.verbose_name to "Device Model" model
- **core**: Add missing attribute Meta.verbose_name to Notes model
- **core**: Add missing attribute Meta.verbose_name to Manufacturer model
- **access**: Add missing attribute Meta.verbos_name to Config Group Software model
- **access**: Add missing attribute Meta.verbos_name to Config Groups model
- **access**: Add missing attribute Meta.ordering Config Groups model
- **access**: Add missing meta field verbose_name to Team model
- **api**: during permission checking if request is HTTP/Options and user is authenticated, allow access
- **api**: during permission checking dont attempt to access view obj if it doesn't exist
- **itam**: Add missing model.Meta attributes ordering and verbose_name

### Refactoring

- **itam**: update device software serializer validator
- **itam**: update device software serializer validator
- **itam**: ensure device is unique for device os model
- ensure filed organization is required
- **config_management**: config_group ref to use full model name
- update serializers to use model `get_url` function
- **core**: ticket comment url name updated to match model name
- Add function `get_url` to tenancy models
- **api**: set fields that are for markdown to use the markdown field
- **task**: Adjust inventory to use API v2 serializer
- **core**: Move ticket validation from is_valid -> validate method
- **core**: Ensure Ticket Linked Serializer works for Item Tickets
- **core**: Ticket Linked Item slash command to use serializer
- **core**: Related ticket slash command to use serializer
- **core**: Ticket Comments to use a single API Endpoint
- **core**: Adjust action choices to be integer
- **config_management**: Adjust rendered config str -> dict
- **itam**: Software Action field changed char -> integer
- **itam**: rename dir viewset -> viewsets
- **config_management**: move config_group_hosts to related table
- update model fields
- **config_management**: update serializer dir name
- **access**: add name to modified field
- **api**: Adjust viewset common so that page_layout is available for base
- **assistance**: Correct viewset dir name to viwsets
- **itam**: Cleanup Device Software model field names.
- **core**: Change history fields after and before to be JSON fields
- **api**: Split common ViewSet class into index/model classes
- **itam**: remove requirement to specify the pk when fetching config

### Tests

- **project_management**: Ensure that project field completed exists when API v2 is rendere
- **core**: Ensure a ticket cant be related to itself
- **itam**: correct test setup for device note viewset
- **settings**: Ensure items returned are from users orgs only for API v2 endpoints
- **project_management**: Ensure items returned are from users orgs only for API v2 endpoints
- **itim**: Correct test case for ticket category returned serializer checks
- **core**: Correct test case for ticket category returned serializer checks
- **core**: Ensure items returned are from users orgs only for API v2 endpoints
- **config_management**: Ensure items returned are from users orgs only for API v2 endpoints
- **assistance**: Ensure items returned are from users orgs only for API v2 endpoints
- **access**: Ensure items returned are from users orgs only for API v2 endpoints
- **itam**: Ensure items returned are from users orgs only for API v2 endpoints
- Test Case for viewsets that confirms returned results from user orgs only
- **itam**: update device model test name Device -> DeviceModel
- **Core**: Ticket linked items API V2 Serializer returned checks
- **Core**: Remove duplicate test for ticket linked items
- **assistance**: Project Taask ticket Viewset Serializer checks
- **assistance**: Problem ticket Viewset Serializer checks
- **assistance**: Incident ticket Viewset Serializer checks
- **assistance**: Change ticket Viewset Serializer checks
- **assistance**: Request ticket Viewset Serializer checks
- **core**: Ticket Test Cases for Viewset Serializer returned
- during delete operation dont include data
- Add ViewSet Returned Serializer Checks to a majority of models
- Test Cases to confirm the correct serializer is returned from ViewSet
- Added skipped test for checking model mandatory values.
- **itam**: Operating System Installs API v2 Field checks
- **itam**: Software Installs API v2 Permission checks
- **itam**: Operating_system Installs API v2 Validation checks
- **itam**: Software Installs API v2 Permission checks
- **itam**: Software Installs API v2 Validation checks
- **itam**: Software Installs API v2 Field checks
- **core**: Ticket serializer checks corrected to use project_id within mock view
- **core**: Ticket comment serializer checks corrected to use mock view
- **core**: Ticket comment category field checks corrected
- **itam**: Update Device Operating System history checks to cater for unique device constratint
- **itam**: Device Operating System API field checks checks
- **itim**: Device Operating System API v2 ViewSet permission checks
- **itam**: Device Operating System Serializer Validation checks
- **core**: remove duplicate functional slash commands
- model get_url function checks
- **core**: move unit tests that check functionality to func test for ticket
- **itam**: Inventory API v2 Serializer Checks
- **core**: Ensure that when ticket is assigned it's status is updated to assigned
- **settings**: External Link API ViewSet permission checks
- **access**: External Link API v2 Serializer Checks
- **functional**: Move request ticket checks from unit
- **functional**: Move functional test cases to relevant functional test dir
- **access**: Organization API v2 Serializer Checks, only super user can create
- **access**: Team User API v2 Serializer Checks
- **access**: Team API v2 Serializer Checks
- **access**: Organization API v2 Serializer Checks
- **project_management**: Organization API v2 ViewSet permission checks
- **core**: Ensure test setup correctly for ticket checks
- **core**: Spend Slash command Checks.
- **core**: Relate Slash command Checks.
- **core**: Ensure that an item that may be linked to a ticket, when its deleted, the ticket link is removed
- **core**: Ensure a non-existing item cant be Linked to a Ticket.
- **core**: Action command Related Item Ticket Slash command checks.
- **core**: Blocked by Slash command Checks.
- **core**: Blocks Slash command Checks.
- **core**: Related Item Ticket Slash command checks.
- **project_management**: Project Task API v2 Serializer Checks
- **itim**: Incident Ticket API v2 Serializer Checks
- **itim**: Problem Ticket API v2 Serializer Checks
- **itim**: Change Ticket API v2 Serializer Checks
- **core**: Request Ticket API v2 Serializer Checks
- **core**: Common Ticket Test Cases for API v2 serializers
- **project_management**: Project Task API field checks
- **itim**: Problem Ticket API field checks
- **itim**: Incident Ticket API field checks
- **itim**: Change Ticket API field checks
- **assistance**: Update request field checks to cater for project and milestone as dicts
- **project_management**: Ensure ticket assigned project for all API v2 ViewSet permission checks
- **project_management**: PRoject_task API v2 ViewSet permission checks
- **itim**: Problem Ticket API v2 ViewSet permission checks
- **itim**: Incident Ticket API v2 ViewSet permission checks
- **itim**: Change Ticket API v2 ViewSet permission checks
- **core**: fix broken tests from 8b701785b3489db567f5ae08c58e28ae76529881 changes
- **core**: Item Ticket API v2 Serializer checks
- **core**: Item Linked Ticket API v2 ViewSet permission checks
- **core**: Related Ticket API v2 Serializer checks
- **core**: Related Ticket API v2 ViewSet permission checks
- **core**: Ticket Comment API v2 Serializer checks
- **core**: Ticket Linked Item API v2 Serializer checks
- **core**: Ticket Comment Category API v2 Serializer checks
- **core**: Ticket Category API v2 Serializer checks
- **itim**: Ticket Linked Item API field checks
- **itim**: Service Ticket URL API field checks
- **itim**: Cluster Ticket URL API field checks
- **itam**: Software Ticket URL API field checks
- **itam**: Operating System Ticket URL API field checks
- **itam**: Device Ticket URL API field checks
- **config_management**: Group Ticket URL API field checks
- **core**: Ticket Comment API v2 ViewSet permission checks
- **core**: Ticket Comment Category API v2 ViewSet permission checks
- **core**: Ticket Category API v2 ViewSet permission checks
- **assistance**: Request Ticket API v2 ViewSet permission checks
- **core**: Ticket Common API v2 ViewSet permission checks
- **core**: Ticket Comment Category API field checks
- **core**: Related Tickets API field checks
- **itim**: Service Linked Tickets API field checks
- **itim**: Cluster Linked Tickets API field checks
- **itam**: Software Linked Tickets API field checks
- **itam**: Operating System Linked Tickets API field checks
- **itam**: device Linked Tickets API field checks
- **core**: Config Group Linked Tickets API field checks
- **core**: Linked Ticket Common API field checks
- **core**: Ticket Linked Items API field checks
- **core**: Ticket Comment API field checks
- **core**: Ticket Category API field checks
- **assistance**: Request Ticket API field checks
- **core**: Ticket Common API field checks
- **settings**: Celery Log API v2 ViewSet permission checks
- **settings**: Celery Log API field checks
- **settings**: User Settings API v2 ViewSet permission checks
- **settings**: User Settings API field checks
- **settings**: App Settings API v2 ViewSet permission checks
- **settings**: App Settings API field checks
- **project_management**: Project API v2 ViewSet permission checks for import user
- **project_management**: Project Serializer Validation clean up
- **project_management**: Project Type API v2 ViewSet permission checks
- **project_management**: Project Type Serializer Validation checks
- **project_management**: Project Type API field checks
- **project_management**: Project State API v2 ViewSet permission checks
- **project_management**: Project state Serializer Validation checks
- **project_management**: Project state API field checks
- **project_management**: Project Milestone API v2 ViewSet permission checks
- **project_management**: Project milestone Serializer Validation checks
- **project_management**: add trace output to Project serializer
- **project_management**: Project Milestone API field checks
- **project_management**: Project API v2 ViewSet permission checks
- **project_management**: Project Serializer Validation checks
- **project_management**: Project API field checks
- **itim**: Port API v2 ViewSet permission checks
- **itim**: Port API field checks
- **itim**: Service API v2 ViewSet permission checks
- **itim**: Service Serializer Validation checks
- **itim**: Service API field checks
- **itim**: Cluster Type API v2 ViewSet permission checks
- **itim**: Cluster Type Serializer Validation checks
- **itam**: Cluster Type API field checks
- **itim**: Cluster API ViewSet permission checks
- **itim**: Cluster Serializer Validation checks
- **itam**: Cluster API field checks
- **itam**: remove Device Ticket API field checks
- **itam**: Device Service API field checks
- **itam**: Device Software API ViewSet permission checks
- **itam**: Device Software Serializer Validation checks
- **itam**: Device Software API field checks
- **itam**: Device Model API ViewSet permission checks
- **itam**: Device Model Serializer Validation checks
- **itam**: Device Model API field checks
- **itam**: Device Type API ViewSet permission checks
- **itam**: Device Type Serializer Validation checks
- **itam**: Device Type API field checks
- **itam**: Software Version Tenancy Model Checks
- **itam**: Software Version API ViewSet permission checks
- **itam**: Software Version Serializer Validation checks
- **itam**: Software Version API field checks
- **itam**: Software Category Version API ViewSet permission checks
- **itam**: Software Category Serializer Validation checks
- **itam**: Software Category Version API field checks
- **itam**: Operating System Version API ViewSet permission checks
- **itam**: Operating System Version Serializer Validation checks
- **itam**: Operating System Version API field checks
- **itam**: Software API ViewSet permission checks
- **itam**: Software Serializer Validation checks
- **itam**: Software API field checks
- **itam**: Operating System Serializer Validation checks
- **itam**: Operating_system API ViewSet permission checks
- **itam**: Operating System API field checks
- **itam**: Device API field checks
- **itam**: Device Serializer Validation checks
- **core**: Device API ViewSet permission checks
- enure correct type checks for url
- **core**: Manufacturer API ViewSet permission checks
- **core**: Manufacturer Serializer Validation checks
- **assistance**: Manufacturer API field checks
- **assistance**: Notes API field checks
- **core**: Notes Serializer Validation checks
- **itim**: Service Note API ViewSet permission checks
- **itam**: Softwaare Note API ViewSet permission checks
- **itam**: Operating System Note API ViewSet permission checks
- **config_management**: Device Note API ViewSet permission checks
- Adjust tests to cater for action choices now being an integer
- **config_management**: Config Groups Note API ViewSet permission checks
- **config_management**: History API ViewSet permission checks
- **config_management**: Config Groups Software API ViewSet permission checks
- **config_management**: Config Groups Software Serializer Validation checks
- **config_management**: Config Groups Software Serializer Validation checks
- **config_management**: Config Groups Serializer Validation checks
- **config_management**: Config Groups API ViewSet permission checks
- **assistance**: Config Group API field checks
- **assistance**: Knowledge Base Category Serializer Validation checks
- **assistance**: ensure is_valid raises exceptions for Knowledge Base Serializer Validation checks
- **assistance**: Knowledge Base Serializer Validation checks
- **assistance**: Knowledge Base Category API field checks
- **assistance**: Knowledge Base API field checks
- **access**: correct organization permission checks to have HTTP/403 not HTTP/405
- **assistance**: Knowledge Base Category API ViewSet permission checks
- **assistance**: Knowledge Base API ViewSet permission checks
- **base**: User API ViewSet permission checks
- **base**: Permission API ViewSet permission checks
- **base**: Content Type API ViewSet permission checks
- **access**: Add missing test cases to Team Users Model
- **access**: Team Users API v2 field checks
- **access**: Team User API ViewSet permission checks
- **access**: Team API v2 field checks
- **api**: API Response Field checks Abstract Class added
- **access**: Organization API v2 field checks
- **access**: Team API ViewSet permission checks
- **access**: Organization API ViewSet permission checks
- **api**: API Permission ViewSet Abstract Class added
- **access**: Team custom tests to ensure that during model field creation, attribute verbose_name is defined and not empty
- **itim**: port placeholder test for invalid port number
- use correct logic when testin field parameters as not being empty or none
- Ensure that during model field creation, attribute verbose_name is defined and not empty
- Ensure that during model field creation, attribute help_text is defined and not empty
- **api**: Ensure models have `Meta.ordering` set and not empty
- **api**: viewset documentation attr check
- **api**: fix index import to correct viewset
- **itam**: Add index viewset checks
- **Settings**: Add index viewset checks
- **project_management**: Add index viewset checks
- **itim**: Add index viewset checks
- **config_management**: Add index viewset checks
- **assistance**: Add index viewset checks
- **access**: Add index viewset checks
- **api**: Add API v2 Endpoint
- **api**: ViewSet checks
- Ensure Models have attribute `page_layout`
- Ensure Models have attribute `table_fields`
- Ensure Models have meta attribute `verbose_name`

## 1.3.1 (2024-11-27)

### Fixes

- **core**: Ensure user cant view tickets in orgs they are not part of

### Tests

- **access**: Add dummy functional test for CI to complete

## 1.3.0 (2024-10-31)

### feat

- **docker**: Add worker service config for SupervisorD
- **docker**: ensure supervisor starts
- **docker**: use correct file location for nginx config
- **docker**: Fail the build if django is not found
- **docker**: Install NginX to serve site
- **docker**: Add supervisord for install
- **docker**: Add gunicorn for install
- update docker image alpine 3.19 ->3.20

### Fixes

- **docker**: Ensure SupervisorD daemon config directory exists.
- **docker**: use alias for static
- **access**: testing of param causing gunicorn to fail
- **docker**: place nginx conf in correct path
- **docker**: gunicorn must call method
- **docker**: Ensure NginX config applied after it's installed
- **docker**: Add proxy params for NginX
- **docker**: Make centurion the default nginx conf
- **docker**: Correct NginX start command

### Refactoring

- **docker**: Switch to entrypoint

## 1.2.2 (2024-10-29)

### Fixes

- **docker**: adjust pyyaml to >-6.0.1

## 1.2.1 (2024-10-22)

### Fixes

- **project_management**: Ensure user cant see projects for organizations they are apart of

### Refactoring

- **project_management**: dont order queryset for project

## 1.2.0 (2024-10-11)

### feat

- update django 5.0.8 -> 5.1.2
- **settings**: Add API filter and search
- **core**: Add API filter of fields external_system and external_ref for projects
- **core**: Add API filter of fields external_system and external_ref to tickets
- **project_management**: increase project field length 50 -> 100 chars
- **core**: increase ticket title field length 50 -> 100 chars
- **core**: Add ability track ticket estimation time for completion
- **core**: Add ability to delete a ticket
- **core**: [Templating Engine] Add template tag concat_strings
- **itim**: Add ticket tab to services
- **itim**: Add ticket tab to clusters
- **itam**: Add ticket tab to software
- **itam**: Add ticket tab to operating systems
- **itam**: Add ticket tab to devices
- **config_management**: Add ticket tab to conf groups
- **core**: Add slash command `link` for linking items to tickets
- **core**: Add to markdown rendering model references
- **core**: Ability to link items to all ticket types
- **core**: add model ticket linked items
- **project_management**: Add project milestones api endpoint
- **project_management**: Add import_project permission and add api serializer
- **core**: great odins beard, remove the checkbox formatting
- **project_management**: Add field is_deleted to projects
- **project_management**: Calculate project completion percentage and display
- **core**: order project categories with parent name if applicable
- **project_management**: Add Project Type to the UI
- **project_management**: Add Project State to the UI
- **project_management**: add priority  field to project model, form and api endpoint
- **project_management**: add organization  field to project form and api endpoint
- **project_management**: add project_type  field to project form
- **project_management**: add external_ref and external_system  field to project model
- **project_management**: add project type field to project model
- **project_management**: add project type api endpoint
- **project_management**: new model project type
- **project_management**: add project state api endpoint
- **project_management**: add project state field to project model
- **project_managemenet**: new model project state
- **project_management**: add field external system to projects
- **core**: validate field milestone for all ticket types
- **core**: Add field milestone to all ticket types
- **project_management**: Add project milestones
- **core**: Add slash command "related ticket" for ticket and ticket comments
- **core**: Suffix username to action comments
- **core**: Add slash command `/spend` for ticket and ticket comments
- **core**: Disable HTML tag rendering for markdown
- **project_management**: remove requirement for code field to be populated
- **core**: Add ticket comment category API endpoint
- **core**: Ability to assign categories to ticket comments
- **core**: Add ticket comment categories
- **core**: Extend all ticket endpoints to contain ticket categories
- **core**: Add ticket category API endpoint
- **core**: Ability to assign categories to tickets
- **core**: Addpage titles to view abstract classes
- **core**: Add ticket categories
- **core**: during markdown render, if ticket ID not found return the tag
- **core**: Add heading anchor plugin to markdown
- **core**: correct markdown formatting for KB articles
- **core**: remove project field from being editable when creating project task
- **core**: Add admonition style
- **project_management**: Validate project task has project set
- **core**: set project ID to match url kwarg
- **core**: Add action comment on title change
- **core**: Add task listts plugin to markdowm
- **core**: Add footnote plugin to markdowm
- **core**: Add admonition plugin to markdowm
- **core**: Add table extension to markdowm
- **core**: Add strikethrough extension to markdowm
- **core**: Add linkify extension to markdowm
- **core**: move markdown parser py-markdown -> markdown-it
- **core**: Add organization column to ticket pages
- **core**: Allow super-user to edit ticket comment source
- **core**: Render linked tickets the same as the rendered markdown link
- **core**: Add project task link for related project task
- **project_management**: Add project duration field
- **core**: Add external ref to tickets if populated
- **core**: Add project task permissions
- **project_management**: Add project tasks
- **api**: Add project tasks endpoint
- **api**: Add projects endpoint
- **api**: Add project management endpoint
- **core**: support negative numbers when Calculating ticket duration for ticket meta and comments
- **core**: Caclulate ticket duration for ticket meta and comments
- **core**: Add edit details to ticket and comments
- **core**: Don't save model history for ticket models
- **core**: add option to allow the prevention of history saving for tenancy models
- **core**: Add project field to tickets allowed fields
- **core**: Update ticket status when assigned/unassigned users/teams
- **core**: Create action comment for subscribed users/teams
- **core**: Create action comment for assigned users/teams
- **core**: adding of more ticket status icons
- **api**: Ticket endpoint dynamic permissions
- **core**: add ticket status badge
- **access**: add ability to fetch dynamic permissions
- **core**: Add delete view for ticket types: request, incident, change and problem
- **api**: when attempting to create a device and it's found within DB, dont recreate, return it.
- **core**: When solution comment posted to ticket update status to solved
- **core**: Add opened by column to ticket indexes
- **core**: permit user to add comment to own ticket
- **core**: Allow OP to edit own Ticket Comment
- **core**: Ticket Comment form submission validation
- **core**: Ticket Comment can be edited by owner
- **core**: Ticket Comment source hidden for non-triage users
- **core**: When fetching allowed ticket comment fields, check against permissions
- **core**: pass request to ticket comment form
- **itam**: Accept device UUID in any case.
- **core**: Add ticket status icon
- **core**: Enable ticket comment created date can be set when an import user
- **api**: Set default values for ticket comment form to match ticket
- **core**: render ticket number `#\d+` links within markdown
- **core**: Use common function for markdown rendering for ticket objects
- **api**: Ensure device can add/edit organization
- **core**: Add api validation for ticket
- **core**: Ensure for tenancy objects that the organization is set
- **core**: Ticket comment orgaanization set to ticket organization
- **core**: colour code related ticket background to ticket type
- **core**: Validate ticket related and prevent duel related entries
- **core**: Validate ticket status field for all ticket types
- **core**: Add ticket action comments on ticket update
- **core**: Add Title bar to ticket form
- **core**: Add field level permission and validation checks
- **core**: Add permission checking to Tickets form
- **access**: add dynamic permissions to Tenancy Permissions
- **api**: Add Tickets endpoint
- **itim**: Add Problem ticket to navigation
- **itim**: Add Incident ticket to navigation
- **itim**: Add Change ticket to navigation
- **assistance**: Add Request ticket to navigation
- **core**: add basic ticketing system
- **development**: add option for including additional stylesheets
- **ui**: add project management icon
- **project_management**: Add manager and users for projects and tasks
- **project_management**: Project task view "view"
- **project_management**: Project task edit view
- **project_management**: Project task delete view
- **project_management**: Project task add view
- **project_management**: Add project task model
- **project_management**: save project history
- **project_management**: add project delete page
- **project_management**: add project edit page
- **project_management**: add project view page
- **project_management**: add project add page
- **project_management**: add project index page
- **project_management**: add interim project model

### Fixes

- ensure model mandatory fields don't specify a default value
- **api**: Ensure user is set to current user for ticket comment
- **core**: remove org field when editing a ticket
- **core**: during validation, if subscribed users not specified, use empty list
- **core**: add missing pagination to ticket comment categories index
- **core**: add missing pagination to ticket categories index
- **project_management**: Ensure project type and state show on index page
- **core**: Add replacement function within ticket validation as `cleaned_data` attribute replacement
- **core**: Ensure the ticket clears project field on project removal
- **core**: Remove ticket fields user has no access to
- **core**: correct logic for slash command `/spend`
- **project_management**: correct project view permissions
- **core**: Correct view permissions for ticket comment category
- **core**: correct url typo for ticket category API endpoint
- **core**: dont attempt to modify field for ticket category API list
- **core**: Dont attempt to render ticket category if none
- **core**: Correct the delete permission
- **core**: correct project task reply link for comments
- **core**: correct project task comment buttons
- **project_management**: correct comment reply url name
- **core**: Generate the correct edit url for tickets
- **core**: Generate the correct comment urls for tickets
- **core**: Redirect to correct url for itim tickets after adding comment
- **core**: correct linked tickets hyperlink address
- **core**: order ticket comments by creation date
- **core**: Ensure for both ticket and comment, external details are unique.
- **core**: Ensure on ticket comment create and update a response is returned
- **core**: Ensure related tricket action comment is trimmed
- **core**: Team assigned to ticket status update
- **api**: ensure ticket_type is set from view var
- **core**: Add ticket fields to ticket types
- **core**: During ticket form validation confirm if value specified/different then default
- **core**: Correctly set the ticket type initial value
- **core**: prevent import user from having permssions within UI
- **api**: correct ticket view links
- **core**: Correct display of ticket status within ticket interface
- **api**: Ensure if device found it is returned
- **core**: Ensure status field remains as part of ticket
- **core**: Correct modified field to correct type for ticket comment
- **api**: Filter ticket comments to match ticket
- **core**: Correct modified field to correct type
- **core**: Ensure new ticket can be created
- **core**: Add `ticket_type` field to import_permissions
- **core**: Ensure that the organization field is available
- **core**: dont remove hidden fields on ticket comment form
- **core**: Correct ticket comment permissions
- **access**: correct permission check to cater for is_global=None
- **core**: return correct redirect path for related ticket form
- **core**: use from ticket title for "blocked by"
- **access**: Don't query for `is_global=None` within `TenancyManager`
- **core**: ensure is_global check does not process null value

### Refactoring

- **core**: Ticket Linked ref render as template
- **core**: migrate ticket enums to own class
- **core**: Ticket validation errors setup for both api and ui
- **core**: for tickets use validation for organization field
- **core**: refine ticket field permission and validation
- reduce action comment spacing
- **core**: update markdown styles
- **core**: migrate ticket number rendering as markdown_it plugin
- **core**: move markdown functions out of ticket model
- **core**: Adjust test layout for itsm and project field based permissions
- **project_management**: migrate projects to new style for views
- **core**: REmove constraint on setting user for ticket comment
- **core**: cache fields allowed during ticket validation
- **core**: dont require specifying ticket status
- **core**: move id to end for rendered ticket link.
- **api**: Ticket (change, incident, problem and request) to static api endpoints
- **api**: make ticket status field mandatory
- **api**: Move core tickets to own ticket endpoints
- **core**: During form validation for a ticket, use defaults if not defined for mandatory fields
- **core**: Ticket form ticket_type to use class var
- **core**: cache permission check for ticket types
- **core**: Move allowed fields logic to own function
- **access**: Add definable parameters to organization mixin
- **access**: cache user_organizations on lookup
- **access**: cache object_organization on lookup

### Tests

- **core**: Ticket Linked item view checks
- **core**: Ticket Linked item permission checks
- **project_management**: Project Milestone api permission checks
- **project_management**: Project TYpe tenancy model checks
- **project_management**: Project Type view checks
- **project_management**: Project Type permission checks
- **project_management**: Project Type core history checks
- **project_management**: Project Type tenancy object checks
- **project_management**: Project State permission checks
- **project_management**: Project State tenancy model checks
- **project_management**: Project State view checks
- **project_management**: Project State core history checks
- **project_management**: Project State tenancy object checks
- **project_management**: Project type API permission checks
- **project_management**: Project state API permission checks
- **project_management**: Project miletone skipped api checks
- **project_management**: Project Milestone tenancy model checks
- **project_management**: Project Milestone view checks
- **project_management**: Project Milestone ui permission checks
- **project_management**: Project Milestone core history checks
- **project_management**: Project Milestone Tenancy object checks
- **core**: Project tenancy model checks
- **core**: Project view checks
- **core**: Project UI permission checks
- **core**: Project API permission checks
- **core**: Project history checks
- **core**: Project Tenancy object checks
- **core**: Ticket comment category API permission checks
- **core**: add missing ticket category view checks
- **core**: ticket comment category tenancy model checks
- **core**: ticket comment category view checks
- **core**: ticket comment category ui permission checks
- **core**: ticket comment category history checks
- **core**: ticket comment category tenancy model checks
- **core**: ticket category API permission checks
- **core**: ticket category history checks
- **core**: ticket category tenancy model checks
- **core**: ticket category model checks
- **core**: view checks
- **core**: ui permissions
- **core**: correct project tests for triage user
- **core**: Project task permission checks
- **core**: Ticket comment API permission checks
- **core**: Ticket comment permission checks
- **core**: Ticket comment Views
- **core**: Tenancy model tests for ticket comment
- **core**: ensure history for ticket models is not saved
- Ensure tenancy models save model history
- **core**: remove duplicated tenancy object tests for ticket model
- **core**: correct triage user test names for allowed field permissions
- **core**: project field permission check for triage user
- **core**: Ticket Action comment checks for related tickets
- **core**: Ticket Action comment checks for subscribing team
- **core**: Ticket Action comment checks for subscribing user
- **core**: Ticket Action comment checks for unassigning team
- **core**: Ticket Action comment checks for assigning team
- **core**: Ticket Action comment checks for un-assigning user
- **core**: Ticket Action comment checks for assigning user
- **core**: Add ticket project field permission check
- **core**: ensure ticket_type tests dont have change value that matches ticket type
- **core**: field based permission tests for add, change, import and triage user
- **api**: Ticket (change, incident, problem and request) api permission checks
- **core**: interim ticket unit tests
- **itam**: Ensure if an attempt to add an existing device via API, it's not recreated and is returned.
- correct typo in test description for `test_model_add_has_permission`
- Add view must have function `get_initial`
- **itam**: Refactor Device tests organization field to be editable.
- Ensure tests add organization to tenancy objects on creation

## 1.1.0 (2024-08-23)

### feat

- **itim**: Dont attempt to apply cluster type config if no type specified.
- **itim**: Service config rendered as part of cluster config
- **itim**: dont force config key, validate when it's required
- **itim**: Services assignable to cluster
- **itim**: Ability to add configuration to cluster type
- **itim**: Ability to add external link to cluster
- **itim**: Ability to add and configure Cluster Types
- **itim**: Add cluster to history save
- **itim**: prevent cluster from setting itself as parent
- **itim**: Ability to add and configure cluster
- **itam**: Track if device is virtual
- **api**: Endpoint to fetch user permissions
- **development**: Add function to filter permissions to those used by centurion
- **development**: Add new template tag `choice_ids` for string list casting
- **development**: Render `model_name_plural` as part of back button
- **development**: add to form field `model_name_plural`
- **development**: render heading if section included
- **base**: create detail view templates
- **itam**: Render Service Config with device config
- **itam**: Display deployed services for devices
- **itim**: Prevent circular service dependencies
- **itim**: Port number validation to check for valid port numbers
- **itim**: Prevent Service template from being assigned as dependent service
- **itim**: Add service template support
- **itim**: Ports for service management
- **itim**: Service Management
- **assistance**: Filter KB articles to target user
- **assistance**: Add date picker to date fields for KB articles
- **assistance**: Dont display expired articles for "view" users
- **base**: add code highlighting to markdown
- **assistance**: Categorised Knowledge base articles
- **itim**: Add menu entry
- **itam**: Ability to add device configuration
- **settings**: New model to allow adding templated links to devices and software

### Fixes

- **settings**: return the rendering of external links to models
- **core**: Ensure when saving history json is correctly formatted
- **itim**: Fix name typo in Add Service button
- Ensure tenancy models have `Meta.verbose_name_plural` attribute
- **base**: Use correct url for back button
- **itim**: ensure that the service template config is also rendered as part of device config
- **itim**: dont render link if no device
- **itim**: Dont show self within service dependencies
- **assistance**: Only return distinct values when limiting KB articles

### Refactoring

- **itim**: Add Cluster type to index page
- **itam**: Knowledge Base now uses details template
- **itam**: Device Type now uses details template
- **itam**: Operating System now uses details template
- **itim**: Service Port now uses details template
- **itam**: Device Model now uses details template
- **config_management**: Config Groups now uses details template
- **itam**: Software Categories now uses details template
- **itam**: manufacturer now uses details template
- **itam**: software now uses details template
- **itam**: device now use details template
- **itim**: services now use details template

### Tests

- **itim**: Cluster Types unit tests
- **itim**: Cluster unit tests
- **itam**: Correct Device Type Model permissions test to use "change" view
- **itam**: Correct Operating System Model permissions test to use "change" view
- **config_management**: Correct Device Model permissions test to use "change" view
- **config_management**: Correct Config Group permissions test to use "change" view
- **itam**: Correct Software Category permissions test to use "change" view
- **core**: Correct manufacturer permissions test to use "change" view
- **itam**: Correct software permissions test to use "change" view
- **model**: test for checking if Meta sub-class has variable verbose_name_plural
- **external_link**: add tests

## 1.0.0 (2024-08-23)

## 1.0.0-b14 (2024-08-12)

### Fixes

- **api**: ensure model_notes is an available field

### Tests

- **access**: test field model_notes

## 1.0.0-b13 (2024-08-11)

### Fixes

- Audit models for validations
- **itam**: Ensure device name is formatted according to RFC1035 2.3.1
- **itam**: Ensure device UUID is correctly formatted
- **config_management**: Ensure that config group can't set self as parent
- **settings**: ensure that the api token cant be saved to notes field

### Tests

- api field checks
- **software**: api field checks

## 1.0.0-b12 (2024-08-10)

### Fixes

- **api**: ensure org mixin is inherited by software view
- **base**: correct project links to github

### Tests

- api field checks

#128 #162
- **teams**: api field checks
- **organization**: api field checks

## 1.0.0-b11 (2024-08-10)

## 1.0.0-b10 (2024-08-09)

## 1.0.0-b9 (2024-08-09)

## 1.0.0-b8 (2024-08-09)

## 1.0.0-b7 (2024-08-09)

## 1.0.0-b6 (2024-08-09)

## 1.0.0-b5 (2024-07-31)

### feat

- add Config groups to API
- **api**: Add device config groups to devices
- **api**: Ability to fetch configgroups from api along with config

### Fixes

- **api**: Ensure device groups is read only

### Tests

- **api**: Field existence and type checks for device
- **api**: test configgroups API fields

## 1.0.0-b4 (2024-07-29)

### feat

- **swagger**: remove `{format}` suffixed doc entries

### Fixes

- release-b3 fixes
- **api**: cleanup team post/get
- **api**: confirm HTTP method is allowed before permission check
- **api**: Ensure that organizations can't be created via the API
- **access**: Team model class inheritance order corrected

### Tests

- confirm that the tenancymanager is called

## 1.0.0-b3 (2024-07-21)

### Fixes

- **itam**: Limit os version count to devices user has access to

## 1.0.0-b2 (2024-07-19)

### Fixes

- **itam**: only show os version once

## 1.0.0-b1 (2024-07-19)

### Fixes

- **itam**: ensure installed operating system count is limited to users organizations
- **itam**: ensure installed software count is limited to users organizations

## 1.0.0-a4 (2024-07-18)

### feat

- **api**: When processing uploaded inventory and name does not match, update name to one within inventory file
- **config_management**: Group name to be entire breadcrumb

### Tests

- ensure inventory upload matches by both serial number and uuid if device name different
- placeholder for moving organization

## 1.0.0-a3 (2024-07-18)

### feat

- **config_management**: Prevent a config group from being able to change organization
- **itam**: On device organization change remove config groups

### Fixes

- **config_management**: dont attempt to do action during save if group being created
- **itam**: remove org filter for device so that user can see installations
- **itam**: remove org filter for operating systems so that user can see installations
- **itam**: remove org filter for software so that user can see installations
- **itam**: Device related items should not be global.
- **itam**: When changing device organization move related items too.

## 1.0.0-a2 (2024-07-17)

### feat

- **api**: Inventory matching of device second by uuid
- **api**: Inventory matching of device first by serial number
- **base**: show warning bar if the user has not set a default organization

### Fixes

- **base**: dont show user warning bar for non-authenticated user
- **api**: correct inventory operating system selection by name
- **api**: correct inventory operating system and it's linking to device
- **api**: correct inventory device search to be case insensitive

## 1.0.0-a1 (2024-07-16)

### BREAKING CHANGE

- squashed DB migrations in preparation for v1.0 release.

### feat

- Administratively set global items org/is_global field now read-only
- **access**: Add multi-tennant manager

### Fixes

- **core**: migrate manufacturer to use new form/view logic
- **settings**: correct the permission to view manufacturers
- **access**: Correct team form fields
- **config_management**: don't exclude parent from field, only self

### Refactoring

- repo preperation for v1.0.0-Alpha-1
- Squash database migrations

### Tests

- tenancy objects
- refactor to single abstract model for inclusion.

## 0.7.0 (2024-07-14)

### feat

- **core**: Filter every form field if associated with an organization to users organizations only
- **core**: add var `template_name` to common view template for all views that require it
- **core**: add Display view to common forms abstract class
- **navigation**: always show every menu for super admin
- **core**: only display navigation menu item if use can view model
- **django**: update 5.0.6 -> 5.0.7
- **core**: add common forms abstract class
- **core**: add common views abstract class
- add postgreSQL database support
- **ui**: add config groups navigation icon
- **ui**: add some navigation icons
- **itam**: update inventory status icon
- **itam**: ensure device software pagination links keep interface on software tab
- "Migrate inventory processing to background worker"
- **access**: enable non-organization django permission checks
- **settings**: Add celery task results index and view page
- **base**: Add background worker
- **itam**: Update Serial Number from inventory if present and Serial Number not set
- **itam**: Update UUID from inventory if present and UUID not set

### Fixes

- **config_management**: Don't allow a config group to assign itself as its parent
- **config_management**: correct permission for deleting a host from config group
- **config_management**: use parent group details to work out permissions when adding a host
- **config_management**: use parent group details to work out permissions
- **itam**: Add missing permissions to software categories index view
- **itam**: Add missing permissions to device types index view
- **itam**: Add missing permissions to device model index view
- **settings**: Add missing permissions to app settings view
- **itam**: Add missing permissions to software index view
- **itam**: Add missing permissions to operating system index view
- **itam**: Add missing permissions to device index view
- **config_management**: Add missing permissions to group views
- **navigation**: always show settings menu entry
- **itam**: cater for fields that are prefixed
- **itam**: Ability to view software category
- **itam**: correct view permission
- **access**: When adding a new team to org ensure parent model is fetched
- **access**: enable org manager to view orgs
- **settings**: restrict user visible organizations to ones they are part of
- **access**: enable org manager to view orgs
- **access**: fetch object if method exists
- **docs**: update docs link to new path
- **access**: correctly set team user parent model to team
- **access**: fallback to django permissions if org permissions check is false
- **access**: Correct logic so that org managers can see orgs they manage
- **base**: add missing content_title to context
- **access**: Enable Organization Manager to view organisations they are assigned to
- **api**: correct logic for adding inventory UUID and serial number to device
- **ui**: navigation alignment and software icon
- **ui**: display organization manager name instead of ID
- **access**: ensure name param exists before attempting to access
- **itam**: dont show none/nil for device fields containing no value
- **itam**: show device model name instead of ID
- **api**: Ensure if serial number from inventory is `null` that it's not used
- **api**: ensure checked uuid and serial number is used for updating
- inventory
- **itam**: only remove device software when not found during inventory upload
- **itam**: only update software version if different
- existing device without uuid not updated when uploading an inventory
- Device Software tab pagination does not work
- **itam**: correct device software pagination

### Refactoring

- adjust views missing add/change form to now use forms
- add navigation menu expand arrows
- migrate views to use new abstract model view classes
- migrate forms to use new abstract model form class
- **access**: Rename Team Button "new user" -> "Assign User"
- **access**: model pk and name not required context for adding a device
- rename field "model notes" -> "Notes"
- remove settings model
- **ui**: increase indentation to sub-menu items
- **itam**: rename old inventory status icon for use with security
- **api**: migrate inventory processing to background worker
- **itam**: only perform actions on device inventory if DB matches inventory item

### Tests

- add test test_view_*_attribute_not_exists_fields for add and change views
- fix test_view_change_attribute_type_form_class to test if type class
- **views**: add test cases for model views
- Add Test case abstract classes to models
- **inventory**: add mocks?? for calling background worker
- **view**: view permission checks
- **inventory**: update tests for background worker changes

## 0.6.0 (2024-06-30)

### feat

- user api token
- **api**: API token authentication
- **api**: abilty for user to create/delete api token
- **api**: create token model

### Fixes

- **user_token**: conduct user check on token view access
- **itam**: use same form for edit and add
- **itam**: dont add field inventorydate if adding new item
- **api**: inventory upload requires sanitization

### Refactoring

- **settings**: use seperate change/view views
- **settings**: use form for user settings
- **tests**: move unit tests to unit test sub-directory

### Tests

- **token_auth**: test authentication method token
- more tests
- add .coveragerc to remove non-code files from coverage report
- Unit Tests TenancyObjects
- Test Cases for TenancyObjects
- tests for checking links from rendered templetes
- **core**: test cases for notes permissions
- **config_management**: config groups history permissions
- **api**: Majority of Inventory upload tests
- **access**: TenancyObject field tests
- **access**: remove skipped api tests for team users

## 0.5.0 (2024-06-17)

### feat

- Setup Organization Managers
- **access**: add notes field to organization
- **access**: add organization manger
- **config_management**: Use breadcrumbs for child group name display
- **config_management**: ability to add host to global group
- **itam**: add a status of "bad" for devices
- **itam**: paginate device software tab
- **itam**: status of device visible on device index page
- API Browser
- **core**: add skeleton http browser
- **core**: Add a notes field to manufacturer/ publisher
- **itam**: Add a notes field to software category
- **itam**: Add a notes field to device types
- **itam**: Add a notes field to device models
- **itam**: Add a notes field to software
- **itam**: Add a notes field to operating system
- **itam**: Add a notes field to devices
- **access**: Add a notes field to teams
- **base**: Add a notes field to `TenancyObjetcs` class
- **settings**: add docs icon to application settings page
- **itam**: add docs icon to software page
- **itam**: add docs icon to operating system page
- **itam**: add docs icon to devices page
- **config_management**: add docs icon to config groups page
- **base**: add dynamic docs icon
- config group software
- **models**: add property parent_object to models that have a parent
- **config_management**: add config group software to group history
- **itam**: render group software config within device rendered config
- **config_management**: assign software action to config group
- sso
- add configuration value 'SESSION_COOKIE_AGE'
- remove development SECRET_KEY and enforce checking for user configured one
- **base**: build CSRF trusted origins from configuration
- **base**: Enforceable SSO ONLY
- **base**: configurable SSO

### Fixes

- **itam**: remove requirement that user needs change device to add notes
- **core**: dont attempt to access parent_object if 'None' during history save
- **config_management**: Add missing parent item getter to model
- **core**: overridden save within SaveHistory to use default attributes
- **access**: overridden save to use default attributes
- History does not delete when item deleted
- **core**: on object delete remove history entries
- inventory upload cant determin object organization
- **api**: ensure proper permission checking
- dont throw an exception during settings load for an item django already checks
- **core**: Add overrides for delete so delete history saved for items with parent model
- **config_management**: correct delete success url
- **base**: remove social auth from nav menu
- **access**: add a team user permissions to use team organization

### Refactoring

- **access**: relocate permission check to own function
- **itam**: move device os tab to details tab
- **itam**: add device change form and adjust view to be non-form
- **itam**: migrate device vie to use manual entered fields in two columns
- **access**: migrate team users view to use forms
- **access**: migrate teams view to use forms
- **access**: migrate organization view to use form
- **base**: cleanup form and prettyfy
- **config_management**: relocate groups views to own directory
- login to use base template
- adjust template block names

### Tests

- **access**: team user model permission check for organization manager
- **access**: team model permission check for organization manager
- **access**: organization model permission check for organization manager
- **access**: add test cases for model delete as organization manager
- **access**: add test cases for model addd as organization manager
- **access**: add test cases for model change as organization manager
- **access**: add test cases for model view as organization manager
- write some more
- **core**: skip invalid tests
- **itam**: tests for device type history entries
- **core**: tests for manufacturer history entries
- move manufacturer to it's parent
- refactor api model permission tests to use an abstract class of test cases
- move tests to the module they belong to
- refactor history permission tests to use an abstract class of test cases
- refactor model permission tests to use an abstract class of test cases
- refactor history entry to have test cases in abstract classes
- **itam**: history entry tests for software category
- **itam**: history entry tests for device operating system version
- **itam**: history entry tests for device operating system
- **itam**: history entry tests for device software
- **itam**: ensure child history is removed on config group software delete
- add placeholder tests
- **itam**: ensure history is removed on software delete
- **itam**: ensure history is removed on operating system delete
- **itam**: ensure history is removed on device model delete
- **config_management**: test history on delete for config groups
- **itam**: ensure history is removed on device delete
- **access**: test team history
- **access**: ensure team user history is created and removed as required
- **access**: ensure history is removed on team delete
- **access**: ensure history is removed on item delete
- **api**: Inventory upload permission checks
- **config_management**: testing of config_groups rendered config
- **config_management**: history save tests for config groups software
- **config_management**: config group software permission for add, change and delete
- **base**: placeholder tests for config groups software
- **base**: basic test for merge_software helper
- during unit tests add SECRET_KEY

## 0.4.0 (2024-06-05)

### feat

- 2024 06 05
- **database**: add mysql support
- **api**: move invneotry api endpoint to '/api/device/inventory'
- **core**: support more history types
- **core**: function to fetch history entry item
- 2024 06 02
- **config_management**: Add button to groups ui for adding child group
- **access**: throw error if no organization added
- **itam**: add delete button to config group within ui
- **itam**: Config groups rendered configuration now part of devices rendered configuration
- **config_management**: Ability to delete a host from a config group
- **config_management**: Ability to add a host to a config group
- **config_management**: ensure config doesn't use reserved config keys
- **config_management**: Config groups rendered config
- **config_management**: add configuration groups
- **api**: add swagger ui for documentation
- **api**: filter software to users organizations
- **api**: filter devices to users organizations
- randomz
- **api**: add org team view page
- API configuration of permissions
- **api**: configure team permissions

### Fixes

- **itam**: ensure device type saves history
- **core**: correct history view permissions
- **config_management**: set config dict keys to be valid ansible variables
- **itam**: correct logic for device add dynamic success url
- **itam**: correct config group link for device
- **config_management**: correct model permissions
- **config_management**: add config management to navigation
- **ui**: remove api entries from navigation
- **api**: check for org must by by type None
- **api**: correct software permissions
- **api**: corrct device permissions
- **api**: permissions for teams
- **api**: correct reverse url lookup to use NS API
- **api**: permissions for organization

### Refactoring

- **access**: cache object so it doesnt have to be called multiple times
- **config_management**: move groups to nav menu
- **api**: migrate devices and software to viewsets
- **api**: move permission check to mixin
- **access**: add team option to org permission check

### Tests

- **api**: placeholder test for inventory
- **settings**: access permission check for app settings
- **settings**: history view permission check for software category
- **settings**: history view permission check for manufacturer
- **settings**: history view permission check for device type
- **settings**: user settings
- **settings**: view permission check for user settings
- refactor core test layout
- **itam**: view permission check for software
- **itam**: view permission check for operating system
- **itam**: view permission check for device model
- **itam**: view permission check for device
- **config_management**: view permission check for config_groups
- **access**: view permission check for team
- **access**: view permission check for organization
- add history entry creation tests for most models
- **config_management**: when adding a host to config group filter out host that are already members of the group
- **config_management**: unit test for config groups model to ensure permissions are working
- **api**: remove tests for os and manufacturer as they are not used in api
- **api**: check model permissions for software
- **api**: check model permissions for devices
- **api**: check model permissions for teams
- **api**: check model permissions for organizations

## 0.3.0 (2024-05-29)

### feat

- Randomz
- **access**: during organization permission check, check to ensure user is logged on
- **history**: always create an entry even if user=none
- **itam**: device uuid must be unique
- **itam**: device serial number must be unique
- 2024 05 26
- **setting**: Enable super admin to set ALL manufacturer/publishers as global
- **setting**: Enable super admin to set ALL device types as global
- **setting**: Enable super admin to set ALL device models as global
- **setting**: Enable super admin to set ALL software categories as global
- **UI**: show build details with page footer
- **software**: Add output to stdout to show what is and has occurred
- 2024 05 25
- **base**: Add delete icon to content header
- **itam**: Populate initial organization value from user default organization for software category creation
- **itam**: Populate initial organization value from user default organization for device type creation
- **itam**: Populate initial organization value from user default organization for device model creation
- **api**: Populate initial organization value from user default organization inventory
- **itam**: Populate initial organization value from user default organization for Software creation
- **itam**: Populate initial organization value from user default organization for operating system creation
- **device**: Populate initial organization value from user default organization
- Add management command software
- **setting**: Enable super admin to set ALL software as global
- **user**: Add user settings panel
- Manufacturer and Model Information
- **itam**: Add publisher to software
- **itam**: Add publisher to operating system
- **itam**: Add device model
- **core**: Add manufacturers
- **settings**: add dummy model for permissions
- **settings**: new module for whole of application settings/globals
- 2024 05 21-23
- **access**: Save changes to history for organization and teams
- **software**: Save changes to history
- **operating_system**: Save changes to history
- **device**: Save changes to history
- **core**: history model for saving model history
- 2024 05 19/20
- **itam**: Ability to add notes to software
- **itam**: Ability to add notes to operating systems
- **itam**: Ability to add notes on devices
- **core**: notes model added to core
- **device**: Record inventory date and show as part of details
- **ui**: Show inventory details if they exist
- **api**: API accept computer inventory

### Fixes

- **settings**: Add correct permissions for team user delete
- **settings**: Add correct permissions for team user view/change
- **settings**: Add correct permissions for team view/change
- **settings**: Add correct permissions for team add
- **settings**: Add correct permissions for team delete
- **access**: correct back link within team view
- **access**: correct url name to be within naming conventions
- **settings**: Add correct permissions for manufacturer / publisher delete
- **settings**: Add correct permissions for manufacturer / publisher add
- **settings**: Add correct permissions for manufacturer / publisher view/update
- **settings**: Add correct permissions for software category delete
- **settings**: Add correct permissions for software category add
- **settings**: Add correct permissions for software category view/update
- **settings**: Add correct permissions for device type delete
- **settings**: Add correct permissions for device type add
- **settings**: Add correct permissions for device type view/update
- **settings**: Add correct permissions for device model delete
- **settings**: Add correct permissions for device model add
- **settings**: Add correct permissions for device model view/update
- **access**: Add correct permissions for organization view/update
- **access**: use established view naming
- **itam**: Add correct permissions for operating system delete
- **itam**: Add correct permissions for operating system add
- **itam**: Add correct permissions for operating system view/update
- **itam**: Add correct permissions for software delete
- **itam**: Add correct permissions for software add
- **itam**: for non-admin user use correct order by fields  for software view/update
- **itam**: Add correct permissions for software view/update
- **itam**: ensure permission_required parameter for view is a list
- **core**: dont save history when no user information available
- **access**: during organization permission check, check the entire list of permissions
- **core**: dont save history for anonymous user
- **access**: during permission check use post request params for an add action
- **user**: on new-user signal create settings row if not exist
- **itam**: ensure only user with change permission can change a device
- **user**: if user settings row doesn't exist on access create
- **access**: adding/deleting team group actions moved to model save/delete method override
- **api**: add teams and permissions to org and teams respectively
- **ui**: correct repo url used
- **api**: device inventory date set to read only
- **software**: ensure management command query correct for migration
- **device**: OS form trying to add last inventory date when empty
- add static files path to urls
- **inventory**: Dont select device_type, use 'null'
- **base**: show "content_title - SITE_TITLE" as site title
- **device**: Read Only field set as required=false
- correct typo in notes templates
- **ui**: Ensure navigation menu entry highlighted for sub items

### Refactoring

- **access**: add to models a get_organization function
- **access**: remove change view
- **itam**: relocation item delete from list to inside device
- **context_processor**: relocate as base
- **itam**: software index does not require created and modified date
- **organizations**: set org field to null if not set
- **itam**: move software categories to settings app
- **itam**: move device types to settings app
- **template**: content_title can be rendered in base

### Tests

- cleanup duplicate tests and minor reshuffle
- **access**: unit testing team user permissions
- **access**: unit testing team permissions
- **settings**: unit testing manufacturer permissions
- **settings**: unit testing software category permissions
- **device_model**: unit testing device type permissions
- **device_model**: unit testing device model permissions
- **organization**: unit testing organization permissions
- **operating_system**: unit testing operating system permissions
- **software**: unit testing software permissions
- **device**: unit testing device permissions
- adjust test layout and update contributing
- **core**: placeholder tests for history component
- **core**: place holder tests for notes model
- **api**: add placeholder tests for inventory

## 0.2.0 (2024-05-18)

### feat

- 2024 05 18
- **itam**: Add Operating System to ITAM models
- **api**: force content type to be JSON for req/resp
- **software**: view software
- 2024 05 17
- **device**: Prevent devices from being set global
- **software**: if no installations found, denote
- **device**: configurable software version
- **software_version**: name does not need to be unique
- **software_version**: set is_global to match software
- **software**: prettify device software action
- **software**: ability to add software versions
- **base**: add stylised action button/text
- **software**: add pagination for index
- **device**: add pagination for index

### Fixes

- **device**: correct software link

## 0.1.0 (2024-05-17)

### feat

- API token auth
- **api**: initial token authentication implementation
- itam and API setup
- **docker**: add settings to store data in separate volume
- **django**: add split settings for specifying additional settings paths
- **api**: Add device config to device
- **itam**: add organization to device installs
- **itam**: migrate app from own repo
- Enable API by default
- Genesis
- **admin**: remove team management
- **admin**: remove group management
- **access**: adjustable team permissions
- **api**: initial work on API
- **template**: add header content icon block
- **tenancy**: Add is_ global field
- **access**: when modifying a team ad/remove user from linked group
- **auth**: include python social auth django application
- Build docker container for release
- **access**: add permissions to team and user
- **style**: format check boxes
- **access**: delete team user form
- **view**: new user
- user who is 'is_superuser' to view everything and not be denied access
- **access**: add org mixin to current views
- **access**: add views for each action for teams
- **access**: add mixin to check organization permissions against user and object
- **account**: show admin site link if user is staff
- **development**: added the debug django app
- **access**: rename structure to access and remove organization app in favour of own implementation
- **account**: Add user password change form
- **urls**: provide option to exclude navigation items
- **structure**: unregister admin pages from organization app not required
- **auth**: Custom Login Page
- **auth**: Add User Account Menu
- **auth**: Setup Login required
- Dyno-magic build navigation from application urls.py
- **structure**: Select and View an individual Organization
- **structure**: View Organizations
- **app**: Add new app structure for organizations and teams
- **template**: add base template
- **django**: add organizations app

### Fixes

- **itam**: device software to come from device org or global not users orgs
- **access**: correct team required permissions
- **fields**: correct autoslug field so it works
- **docker**: build wheels then install

### Refactoring

- button to use same selection colour
- **access**: remove inline form for org teams
- rename app from itsm -> app
- **access**: dont use inline formset
- **views**: move views to own directory
- **access**: addjust org and teams to use different view per action

### Tests

- interim unit tests

## 0.0.1 (2024-05-06)
