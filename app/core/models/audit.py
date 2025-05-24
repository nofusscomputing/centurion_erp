from django.conf import settings
from django.contrib.auth.models import ContentType
from django.db import models
from django.core.exceptions import ValidationError

from core.models.centurion import (
    CenturionModel,
    CenturionSubModel,
)




class CenturionAudit(
    CenturionModel,
):
    """Centurion Audit History

    This model is responsible for recording change to a model. The saving of
    model history is via the `delete` and `save` signals

    Args:
        CenturionModel (_type_): Centurion Model attributes, functions and method
        TenancyObject (_type_): Centurion Tenancy Abstract model.
    """

    _audit_enabled: bool = False
    """Don't Save audit history for audit history model"""

    _notes_enabled: bool = False
    """Don't create notes table for istory model"""

    model_notes = None

    class Meta:

        # db_table = 'centurion_audit'
        db_table = 'core_audithistory'

        ordering = [
            '-created'
        ]

        verbose_name = 'Model History'

        verbose_name_plural = 'Model Histories'


    content_type = models.ForeignKey(
        ContentType,
        blank= True,
        help_text = 'Model this history is for',
        null = False,
        on_delete = models.CASCADE,
        validators = [
            CenturionModel.validate_field_not_none,
        ],
        verbose_name = 'Content Model'
    )

    before = models.JSONField(
        blank = True,
        help_text = 'Value before Change',
        null = True,
        validators = [
            CenturionModel.validate_field_not_none,
        ],
        verbose_name = 'Before'
    )


    after = models.JSONField(
        blank = True,
        help_text = 'Value Change to',
        null = True,
        validators = [
            CenturionModel.validate_field_not_none,
        ],
        verbose_name = 'After'
    )


    class Actions(models.IntegerChoices):
        ADD    = 1, 'Create'
        UPDATE = 2, 'Update'
        DELETE = 3, 'Delete'

    action = models.IntegerField(
        blank = False,
        choices = Actions,
        help_text = 'History action performed',
        null = True,
        validators = [
            CenturionModel.validate_field_not_none,
        ],
        verbose_name = 'Action'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = False,
        help_text = 'User whom performed the action',
        null = False,
        on_delete = models.DO_NOTHING,
        validators = [
            CenturionModel.validate_field_not_none,
        ],
        verbose_name = 'User'
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



    def clean_fields(self, exclude: set = None):
        """Clean Model Fields

        The Audit Sub-Model that inherits from this model must implement this
        method so as to populate the history fields with the history data.

        Args:
            exclude (set, optional): List of fields to exclude. Defaults to
                None.

        Raises:
            NotImplementedError: The Audit sub-model that inheirts has failed
                to implement this method.
        """

        if type(self) is not CenturionAudit:

            raise NotImplementedError(
                'Audit sub models must implement this method to populate fields'
            )

        super().clean_fields( exclude = exclude )



    def get_model_history(self, model: models.Model) -> bool:
        """Populate fields `self.before` and `self.after`

        Pass in the model that changed and this function will read values
        `model.before` and `model.after` to populate the history table.

        **Note:** Audit history expects all models to call and save to an
        attribute `before` `self.__dict__` and after save to an attribute
        called `after`. Prior to calling the after, you must refresh from the
        database.

        Args:
            model (models.Model): The model to get the history for

        Returns:
            True (bool): History fields populated
            Fail (bool): History fields not populated
        """

        if not hasattr(model, 'before'):

            raise ValidationError(
                code = 'model_missing_before_data',
                message = 'Unable to save model history as the "before" data is missing.'
            )

        if not hasattr(model, 'after'):

            raise ValidationError(
                code = 'model_missing_after_data',
                message = 'Unable to save model history as the "after" data is missing.'
            )

        if model.before == model.after:

            raise ValidationError(
                code = 'before_and_after_same',
                message = 'Unable to save model history.The "before" and "after" data is the same.'
            )


        # loop through before and after and remove from after any fields that are the same.



        return None



class AuditMetaModel(
    CenturionAudit,
    CenturionSubModel,
):

    model_notes = None

    class Meta:
        abstract = True
        proxy = False



    def clean_fields(self, exclude = None):

        if getattr(self, 'model', None):

            if not self.get_model_history(self.model):

                raise ValidationError(
                    code = 'did_not_process_history',
                    message = 'Unable to process the history.'
                )

        else:

                raise ValidationError(
                    code = 'no_model_supplied',
                    message = 'Unable to process the history, no model was supplied.'
                )


        super().clean_fields(exclude = exclude)
