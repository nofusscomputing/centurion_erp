from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from access.fields import AutoLastModifiedField
from access.models.company_base import (
    Company
)

from centurion.lib.decorators import depreciate

from core.models.centurion import CenturionModel

from core.models.manufacturer import Manufacturer

from settings.models.app_settings import AppSettings



@depreciate(
    depreciated_in = '1.36.0',
    removed_in = '2.0',
    replacement = 'itam.ITAssetModel',
    skip_tests = True,
)
class DeviceModel(
    CenturionModel
):    # pragma: no cover

    model_tag = 'device_model-'


    class Meta:

        ordering = [
            'manufacturer',
            'name',
        ]

        verbose_name = 'Device Model'

        verbose_name_plural = 'Device Models'


    migrated_id = models.ForeignKey(
        to = 'itam.ITAssetModel',
        blank = True,
        help_text = 'PK of the model migrated to',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'New Model PK'
    )

    name = models.CharField(
        blank = False,
        help_text = 'The items name',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    manufacturer_old = models.ForeignKey(
        Manufacturer,
        blank = True,
        help_text = 'Manufacturer this model is from',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Manufacturer'
    )

    manufacturer = models.ForeignKey(
        Company,
        blank = True,
        help_text = 'Manufacturer this model is from',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'device_models',
        verbose_name = 'Manufacturer'
    )

    modified = AutoLastModifiedField()

    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    'manufacturer',
                    'name',
                    'organization',
                    'created',
                    'modified'
                ]
            ]
        },
        "detail": [
            {
                "name": "Details",
                "slug": "details",
                "sections": [
                    {
                        "layout": "double",
                        "left": [
                            'organization',
                            'manufacturer',
                            'name',
                        ],
                        "right": [
                            'model_notes',
                            'created',
                            'modified',
                        ]
                    }
                ]
            },
            {
                "name": "Knowledge Base",
                "slug": "kb_articles",
                "sections": [
                    {
                        "layout": "table",
                        "field": "knowledge_base",
                    }
                ]
            },
            {
                "name": "Notes",
                "slug": "notes",
                "sections": []
            }
        ],
        "table": [
            'manufacturer',
            'name',
            'organization',
            'created',
            'modified'
        ]
    }


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.it_asset_model_is_global:

            self.organization = app_settings.global_organization

        super().clean()


    def __str__(self):

        if self.manufacturer:

            return self.manufacturer.name + ' ' + self.name

        return self.name


    def migrate(self) -> None:

        new_model = apps.get_model(
            app_label = 'itam',
            model_name = 'itassetmodel'
        )

        history_content_type = ContentType.objects.get_for_model(new_model())

        new_history_model = apps.get_model(
            app_label = new_model._meta.app_label,
            model_name = str(new_model().get_history_model_name()).lower()
        )

        new_notes_model = apps.get_model(
            app_label = new_model._meta.app_label,
            model_name = str(f'{new_model._meta.object_name}CenturionModelNote').lower()
        )

        system_user = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(
            username = 'system'
        ).first()

        new_model.context[self._meta.model_name] = system_user

        current_model  = self

        created_object = ''
        try:

            type(self).context['logger'].info(f"Begin migrating {self.pk} - {getattr(current_model.manufacturer, 'name', '')} {current_model.name}.")

            device_type = None
            for device in current_model.device_set.all():

                if device.device_type is not None:
                    device_type = device.device_type
                    break


            created_object = new_model.objects.create(
                name = current_model.name,
                model_notes = current_model.model_notes,
                device_type = device_type,
                manufacturer = current_model.manufacturer,
                imei = False,
                mac_address = False,
                puk = False,
                puk_pin = False,
                serial_number = False,
                organization = current_model.organization,
                created = current_model.created,
                modified = current_model.modified
            )

            type(self).context['logger'].info(f'Migrated {self.pk} to {created_object.pk}.')

            notes_model = apps.get_model(
                app_label = current_model._meta.app_label,
                model_name = str(f'{current_model._meta.object_name}CenturionModelNote').lower()
            )

            type(self).context['logger'].info(f'Begin migrate notes for {self.pk}.')

            for notes_entry in notes_model.objects.filter(
                model_id = current_model.pk
            ):

                new_notes_model.objects.create(
                    body = notes_entry.body,
                    created_by = notes_entry.created_by,
                    modified_by = notes_entry.modified_by,

                    model = created_object,

                    organization = notes_entry.organization,
                    created = notes_entry.created,
                    modified = notes_entry.modified,


                )

                type(self).context['logger'].info(f'Migrate note {notes_entry.pk} to {new_notes_model.pk}.')


            type(self).context['logger'].info(f'Begin migrate audit entries for {self.pk}.')

            history_model = apps.get_model(
                app_label = current_model._meta.app_label,
                model_name = str(current_model.get_history_model_name()).lower()
            )

            for audit_entry in history_model.objects.filter(
                model_id = current_model.pk
            ):

                new_audit_entry = new_history_model.objects.create(
                    content_type = history_content_type,

                    model = created_object,

                    before = audit_entry.before,
                    after = audit_entry.after,
                    action = audit_entry.action,
                    user = audit_entry.user,
                    organization = audit_entry.organization,
                    created = audit_entry.created

                )

                type(self).context['logger'].info(f'Migrate audit_entry {audit_entry.pk} to {new_audit_entry.id}.')


            current_model.migrated_id = created_object
            current_model.save()

        except Exception as exc:
            type(self).context['logger'].exception(exc)


            if hasattr( created_object, 'pk'):    # Remove migrated object

                type(self).context['logger'].notice('Begin reverting created notes.')

                for note in new_notes_model.objects.filter(
                    model = created_object
                ):

                    type(self).context['logger'].notice(f'Reverting note {note.pk}.')

                    note.delete()


                type(self).context['logger'].notice('Begin reverting created audit entries.')

                for history_model in new_history_model.objects.filter(
                    model = created_object
                ):

                    type(self).context['logger'].notice(f'Reverting note {history_model.pk}.')

                    history_model.delete()


                type(self).context['logger'].notice(f'Revert created model {created_object.pk}.')

                created_object.delete()


        del new_model.context[self._meta.model_name]

        type(self).context['logger'].info(f"Completed migration for {self.pk} - {getattr(self.manufacturer, 'name', '')} {self.name}.")
