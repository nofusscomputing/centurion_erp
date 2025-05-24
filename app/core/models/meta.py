import sys
import types

from django.apps import apps
from django.db import models
from django.utils.module_loading import import_string



module_path = f'centurion.models.meta'

if module_path not in sys.modules:

    sys.modules[module_path] = types.ModuleType(module_path)


if apps.models_ready:

    existing_models = { m.__name__ for m in apps.get_models() }

    for model in apps.get_models():

        if not getattr(model, '_audit_enabled', False):
            continue

        name = model.__name__

        audit_meta_name = model().get_history_model_name()

        if audit_meta_name in existing_models:
            continue


        AuditMetaModel = type(
            audit_meta_name,
            ( import_string("core.models.audit.AuditMetaModel"), ),
            {
                '__module__': module_path,
                '__qualname__': audit_meta_name,
                '__doc__': f'Auto-generated meta model for {name} Audit History.',
                'Meta': type('Meta', (), {
                            'app_label': model._meta.app_label,
                            'db_table': model._meta.db_table + '_history',
                            'managed': True,
                            'verbose_name': model._meta.verbose_name + ' History',
                            'verbose_name_plural': model._meta.verbose_name + ' Histories',
                        }),
                'model': models.ForeignKey(
                    model,
                    blank = False,
                    help_text = 'Model this history belongs to',
                    null = False,
                    on_delete = models.CASCADE,
                    related_name = 'audit_history',
                    verbose_name = 'Model',
                )
            }
        )

        setattr(sys.modules[module_path], audit_meta_name, AuditMetaModel)
