from django.conf import settings
from django.contrib.auth.models import ContentType
from django.db import models

from rest_framework.reverse import reverse

from access.fields import AutoCreatedField
from access.models.tenant import Tenant
from access.models.tenancy import TenancyObject

from core.models.centurion import (
    CenturionModel,
)

from core.lib.feature_not_used import FeatureNotUsed



class ModelHistoryOld:
    """ Old Model History

    This class exists until the other models that rely upon these attributes
    and functions are refactored to not rely upon these functions.
    """

    save_model_history: bool = False

    model_notes = None

    is_global = None

    child_history_models = [
        'configgrouphostshistory',
        'configgroupsoftwarehistory',
        'deviceoperatingsystemhistory',
        'devicesoftwarehistory',
        'projectmilestonehistory',
    ]
    """Child History Models

    This list is currently used for excluding child models from the the history
    select_related query.

    Returns:
        list: Child history models.
    """

    page_layout: list = []

    table_fields: list  = [
        'created',
        'action',
        'content',
        'user',
        'nbsp',
        [
            'before',
            'after'
        ]
    ]


    def get_related_field_name(self, model) -> str:

        meta = getattr(model, '_meta')

        for related_object in getattr(meta, 'related_objects', []):

            if getattr(model, related_object.name, None):

                return related_object.name

        # return related_field_name
        return ''


    def get_serialized_model_field(self, context):

        model = None

        model = getattr(self, self.get_related_field_name( self ))

        model = model.get_serialized_model(context).data

        return model


    def get_serialized_child_model_field(self, context):

        model = {}

        parent_model = getattr(self, self.get_related_field_name( self ))

        child_model = getattr(parent_model, self.get_related_field_name( parent_model ), None)

        if child_model is not None:

            model = child_model.get_serialized_child_model(context).data

        return model


    def get_url_kwargs(self) -> dict:

        parent_model = getattr(self, self.get_related_field_name( self ))

        return {
            'app_label': parent_model.model._meta.app_label,
            'model_name': parent_model.model._meta.model_name,
            'model_id': parent_model.model.pk,
            'pk': parent_model.pk
        }


    def get_url_kwargs_notes(self):

        return FeatureNotUsed


    def get_url( self, request = None ) -> str:

        if request:

            return reverse(f"v2:_api_v2_model_history-detail", request=request, kwargs = self.get_url_kwargs() )

        return reverse(f"v2:_api_v2_model_history-detail", kwargs = self.get_url_kwargs() )



# class CenturionAudit(
class ModelHistory(
    ModelHistoryOld,
    TenancyObject,
):
    """Centurion Audit History

    This model is responsible for recording change to a model. The saving of
    model history is via the `delete` and `save` signals

    Args:
        ModelHistoryOld (_type_): Old Model attributes and functions due for removal.
        CenturionModel (_type_): Centurion Model attributes, functions and method
        TenancyObject (_type_): Centurion Tenancy Abstract model.
    """

    audit_enabled: bool = False


    class Meta:

        # db_table = 'centurion_audit'
        db_table = 'core_model_history'

        ordering = [
            '-created'
        ]

        verbose_name = 'Model History'

        verbose_name_plural = 'Model Histories'


    id = models.AutoField(
        blank=False,
        help_text = 'ID of the item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    organization = models.ForeignKey(
        Tenant,
        blank = False,
        help_text = 'Tenancy this belongs to',
        null = True,
        on_delete = models.CASCADE,
        related_name = '+',
        # validators = [
        #     CenturionModel.validate_field_not_none,
        # ],
        verbose_name = 'Tenant'
    )

    content_type = models.ForeignKey(
        ContentType,
        blank= True,
        help_text = 'Model this history is for',
        null = False,
        on_delete = models.CASCADE,
        # validators = [
        #     CenturionModel.validate_field_not_none,
        # ],
        verbose_name = 'Content Model'
    )

    before = models.JSONField(
        blank = True,
        default = None,
        help_text = 'Value before Change',
        null = True,
        # validators = [
        #     CenturionModel.validate_field_not_none,
        # ],
        verbose_name = 'Before'
    )


    after = models.JSONField(
        blank = True,
        default = None,
        help_text = 'Value Change to',
        null = True,
        # validators = [
        #     CenturionModel.validate_field_not_none,
        # ],
        verbose_name = 'After'
    )


    class Actions(models.IntegerChoices):
        ADD    = 1, 'Create'
        UPDATE = 2, 'Update'
        DELETE = 3, 'Delete'

    action = models.IntegerField(
        blank = False,
        choices = Actions,
        default = None,
        help_text = 'History action performed',
        null = True,
        # validators = [
        #     CenturionModel.validate_field_not_none,
        # ],
        verbose_name = 'Action'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = False,
        help_text = 'User whom performed the action',
        null = True,
        on_delete = models.DO_NOTHING,
        # validators = [
        #     CenturionModel.validate_field_not_none,
        # ],
        verbose_name = 'User'
    )

    created = AutoCreatedField(
        editable = True
    )



    page_layout: list = []

    table_fields: list  = [
        'created',
        'action',
        'content',
        'user',
        'nbsp',
        [
            'before',
            'after'
        ]
    ]
