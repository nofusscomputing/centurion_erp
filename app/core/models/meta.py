import sys
import types

from django.apps import apps
from django.db import models
from django.utils.module_loading import import_string

# Note: Only included so that it can be picked up.
# in future when model referenced, this include statement may be repoved.
from access.models.company_base import Company    # pylint: disable=W0611:unused-import
from access.models.role import Role   # pylint: disable=W0611:unused-import
## EoF Include block


module_path = f'centurion.models.meta'

if module_path not in sys.modules:

    sys.modules[module_path] = types.ModuleType(module_path)


if apps.models_ready:

    existing_models = { m.__name__ for m in apps.get_models() }

    for model in apps.get_models():

        name = model.__name__

        if getattr(model, '_audit_enabled', False):

            audit_meta_name = model().get_history_model_name()

            if audit_meta_name in existing_models:
                continue


            related_name = 'audit_history'
            if model._is_submodel:

                related_name = '+'


            AuditMetaModel = type(
                audit_meta_name,
                ( import_string("core.models.audit.AuditMetaModel"), ),
                {
                    '__module__': module_path,
                    '__qualname__': audit_meta_name,
                    '__doc__': f'Auto-generated meta model for {name} Audit History.',
                    'Meta': type('Meta', (), {
                                'app_label': model._meta.app_label,
                                'db_table': model._meta.db_table + '_audithistory',
                                'managed': True,
                                'ordering': [ '-created' ],
                                'verbose_name': model._meta.verbose_name + ' History',
                                'verbose_name_plural': model._meta.verbose_name + ' Histories',
                            }),
                    'model': models.ForeignKey(
                        model,
                        blank = False,
                        help_text = 'Model this history belongs to',
                        null = False,
                        on_delete = models.CASCADE,
                        related_name = related_name,
                        verbose_name = 'Model',
                    )
                }
            )

            setattr(sys.modules[module_path], audit_meta_name, AuditMetaModel)


        if getattr(model, '_notes_enabled', False):

            notes_meta_name = f'{model._meta.object_name}CenturionModelNote'

            if notes_meta_name in existing_models:
                continue


            NotesMetaModel = type(
                notes_meta_name,
                ( import_string("core.models.centurion_notes.NoteMetaModel"), ),
                {
                    '__module__': module_path,
                    '__qualname__': notes_meta_name,
                    '__doc__': f'Auto-generated meta model for {name} Notes.',
                    'Meta': type('Meta', (), {
                                'app_label': model._meta.app_label,
                                'db_table': model._meta.db_table + '_centurionmodelnote',
                                'managed': True,
                                'verbose_name': model._meta.verbose_name + ' Note',
                                'verbose_name_plural': model._meta.verbose_name + ' Notes',
                            }),
                    'model': models.ForeignKey(
                        model,
                        blank = False,
                        help_text = 'Model this note belongs to',
                        null = False,
                        on_delete = models.CASCADE,
                        related_name = '+',
                        verbose_name = 'Model',
                    )
                }
            )

            setattr(sys.modules[module_path], notes_meta_name, NotesMetaModel)
