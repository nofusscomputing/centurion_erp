from django.apps import apps
from django.db.models.signals import (
    post_migrate,
)
from django.dispatch import receiver

from core.mixins.centurion import Centurion


@receiver(post_migrate, dispatch_uid="centurion_model_migrate")
def centurion_model_migrate(sender, **kwargs):


    if sender.label != 'core':
        return

    print('\n\nCenturion Model Migration Signal.....\n')

    models: list[ dict ] = [
        {
            'app_label': 'access',
            'model_name': 'Tenant',
            'history_model_name': 'OrganizationHistory',
            'notes_model_name': 'OrganizationNotes'
        },
        {
            'app_label': 'assistance',
            'model_name': 'KnowledgeBase',
            'history_model_name': 'KnowledgeBaseHistory',
            'notes_model_name': 'KnowledgeBaseNotes'
        },
        {
            'app_label': 'assistance',
            'model_name': 'KnowledgeBaseCategory',
            'history_model_name': 'KnowledgeBaseCategoryHistory',
            'notes_model_name': 'KnowledgeCategoryBaseNotes'
        },
        {
            'app_label': 'config_management',
            'model_name': 'ConfigGroupHosts',
            'history_model_name': 'ConfigGroupHostsHistory',
            'notes_model_name': None
        },
        {
            'app_label': 'config_management',
            'model_name': 'ConfigGroupSoftware',
            'history_model_name': 'ConfigGroupSoftwareHistory',
            'notes_model_name': None
        },
        {
            'app_label': 'config_management',
            'model_name': 'ConfigGroups',
            'history_model_name': 'ConfigGroupsHistory',
            'notes_model_name': 'ConfigGroupNotes'
        },
        {
            'app_label': 'core',
            'model_name': 'Manufacturer',
            'history_model_name': 'ManufacturerHistory',
            'notes_model_name': 'ManufacturerNotes'
        },
        {
            'app_label': 'core',
            'model_name': 'TicketCategory',
            'history_model_name': 'TicketCategoryHistory',
            'notes_model_name': 'TicketCategoryNotes'
        },
        {
            'app_label': 'core',
            'model_name': 'TicketCommentCategory',
            'history_model_name': 'TicketCommentCategoryHistory',
            'notes_model_name': 'TicketCommentCategoryNotes'
        },
        {
            'app_label': 'devops',
            'model_name': 'CheckIn',
            'history_model_name': None,
            'notes_model_name': None
        },
        {
            'app_label': 'devops',
            'model_name': 'FeatureFlag',
            'history_model_name': 'FeatureFlagHistory',
            'notes_model_name': 'FeatureFlagNotes'
        },
        {
            'app_label': 'devops',
            'model_name': 'GitGroup',
            'history_model_name': 'GitGroupHistory',
            'notes_model_name': 'GitGroupNotes'
        },
        {
            'app_label': 'devops',
            'model_name': 'GitRepository',
            'history_model_name': None,
            'notes_model_name': None
        },
        {
            'app_label': 'devops',
            'model_name': 'GitHubRepository',
            'history_model_name': 'GitHubHistory',
            'notes_model_name': 'GitHubRepositoryNotes'
        },
        {
            'app_label': 'devops',
            'model_name': 'GitLabRepository',
            'history_model_name': 'GitlabHistory',
            'notes_model_name': 'GitLabRepositoryNotes'
        },
        {
            'app_label': 'itam',
            'model_name': 'Device',
            'history_model_name': 'DeviceHistory',
            'notes_model_name': 'DeviceNotes'
        },
        {
            'app_label': 'itam',
            'model_name': 'DeviceModel',
            'history_model_name': 'DeviceModelHistory',
            'notes_model_name': 'DeviceModelNotes'
        },
        {
            'app_label': 'itam',
            'model_name': 'DeviceType',
            'history_model_name': 'DeviceTypeHistory',
            'notes_model_name': 'DeviceTypeNotes'
        },
        {
            'app_label': 'itam',
            'model_name': 'OperatingSystem',
            'history_model_name': 'OperatingSystemHistory',
            'notes_model_name': 'OperatingSystemNotes'
        },
        {
            'app_label': 'itam',
            'model_name': 'OperatingSystemVersion',
            'history_model_name': 'OperatingSystemVersionHistory',
            'notes_model_name': 'OperatingSystemVersionNotes'
        },
        {
            'app_label': 'itam',
            'model_name': 'Software',
            'history_model_name': 'SoftwareHistory',
            'notes_model_name': 'SoftwareNotes'
        },
        {
            'app_label': 'itam',
            'model_name': 'SoftwareCategory',
            'history_model_name': 'SoftwareCategoryHistory',
            'notes_model_name': 'SoftwareCategoryNotes'
        },
        {
            'app_label': 'itam',
            'model_name': 'SoftwareVersion',
            'history_model_name': 'SoftwareVersionHistory',
            'notes_model_name': 'SoftwareVersionNotes'
        },
        {
            'app_label': 'itim',
            'model_name': 'Cluster',
            'history_model_name': 'ClusterHistory',
            'notes_model_name': 'ClusterNotes'
        },
        {
            'app_label': 'itim',
            'model_name': 'ClusterType',
            'history_model_name': 'ClusterTypeHistory',
            'notes_model_name': 'ClusterTypeNotes'
        },
        {
            'app_label': 'itim',
            'model_name': 'Port',
            'history_model_name': 'PortHistory',
            'notes_model_name': 'PortNotes'
        },
        {
            'app_label': 'itim',
            'model_name': 'Service',
            'history_model_name': 'ServiceHistory',
            'notes_model_name': 'ServiceNotes'
        },
        {
            'app_label': 'project_management',
            'model_name': 'Project',
            'history_model_name': 'ProjectHistory',
            'notes_model_name': 'ProjectNotes'
        },
        {
            'app_label': 'project_management',
            'model_name': 'ProjectMilestone',
            'history_model_name': 'ProjectMilestoneHistory',
            'notes_model_name': 'ProjectMilestoneNotes'
        },
        {
            'app_label': 'project_management',
            'model_name': 'ProjectState',
            'history_model_name': 'ProjectStateHistory',
            'notes_model_name': 'ProjectStateNotes'
        }
    ]


    print(f'Found {len( models )} models to process......')
    for app_label,  model_name, history_model_name, notes_model_name in [
        (a[1], b[1], c[1], d[1] ) for a,b,c,d in [x.items() for x in models]
    ]:

        print(f'Processing model {model_name}:')

        model = apps.get_model(
            app_label = app_label,
            model_name = model_name
        )

        if(
            not issubclass(model, Centurion)
        ):
            print(f'Skipping model {model_name} as it is not a CenturionModel.')
            continue


        print(f"    Audit History is enabled={getattr(model, '_audit_enabled', False)}.")

        if getattr(model, '_audit_enabled', False):


            try:

                if history_model_name is None:

                    raise LookupError('No history model to migrate')

                original_history = apps.get_model(
                    app_label = app_label,
                    model_name = history_model_name
                )


                try:

                    audit_history = apps.get_model(
                        app_label = app_label,
                        model_name = model.get_history_model_name( model )
                    )

                    history = original_history.objects.filter().exclude( user = None )

                    print(f'        Found {len(history)} history entries to migrate.')

                    for entry in history:

                        try:

                            entry_model = entry.model
                            if hasattr(entry, 'child_model'):
                                entry_model = entry.child_model

                            migrated_history = audit_history.objects.create(
                                organization = entry.organization,
                                content_type = entry.content_type,
                                model = entry_model,
                                before = entry.before,
                                after = entry.after,
                                action = entry.action,
                                user = entry.user,
                                created = entry.created
                            )

                            id = entry.id

                            print(f'        Migrated History {history_model_name}={id} to'
                                f' {model.get_history_model_name( model )}={migrated_history.id}.')

                            entry.delete()

                            print(f'        Removed {history_model_name}={id} from database.')

                        except Exception as e:
                            print(
                                f"        Exception {e.__class__.__name__} occured:"+"\n" \
                                    "            "+f'{e}')


                except LookupError as e:
                    print(f"Model {model.get_history_model_name( model )} is missing: {e}")


            except LookupError as e:    # Model does not exist
                print(f'Model {history_model_name} does not exist: {e}')


        print(f"    Model Notes is enabled={getattr(model, '_notes_enabled', False)}.")

        if getattr(model, '_notes_enabled', False):

            try:

                if notes_model_name is None:

                    raise LookupError('No notes model to migrate')


                original_notes = apps.get_model(
                    app_label = app_label,
                    model_name = notes_model_name
                )


                try:

                    model_notes = apps.get_model(
                        app_label = app_label,
                        model_name = model._meta.object_name + 'CenturionModelNote'
                    )

                    notes = original_notes.objects.all()

                    print(f'        Found {len(notes)} model note entries to migrate.')

                    for entry in notes:

                        try:

                            migrated_note = model_notes.objects.create(
                                organization = entry.organization,
                                body = entry.content,
                                created_by = entry.created_by,
                                modified_by = entry.modified_by,
                                model = entry.model,
                                content_type = entry.content_type,
                                created = entry.created,
                                modified = entry.modified
                            )

                            id = entry.id

                            print(f'        Migrated Notes {notes_model_name}={id} to'
                                f" {model._meta.object_name + 'CenturionModelNote'}="
                                    f'{migrated_note.id}.')

                            entry.delete()

                            print(f'        Removed {notes_model_name}={id} from database.')


                        except Exception as e:
                            print(f"Exception {e.__class__.__name__} occured:\n\s\s\s\s{e}")


                except LookupError as e:
                    print(f"Model {model._meta.object_name + 'CenturionModelNote'} is missing: {e}")


            except LookupError as e:    # Model does not exist
                print(f'Model {notes_model_name} does not exist: {e}')

    print(f'Migration from old history and notes tables to new tables completed.')
