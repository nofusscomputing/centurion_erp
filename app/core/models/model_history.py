from django.contrib.auth.models import ContentType, User
from django.db import models

from rest_framework.reverse import reverse

from access.fields import AutoCreatedField
from access.models import TenancyObject



class ModelHistory(
    TenancyObject
):


    class Meta:

        db_table = 'core_model_history'

        ordering = [
            '-created'
        ]

        verbose_name = 'History'

        verbose_name_plural = 'History'


    class Actions(models.IntegerChoices):
        ADD    = 1, 'Create'
        UPDATE = 2, 'Update'
        DELETE = 3, 'Delete'


    model_notes = None    # model notes not required for this model

    before = models.JSONField(
        blank = True,
        default = None,
        help_text = 'JSON Object before Change',
        null = True,
        verbose_name = 'Before'
    )


    after = models.JSONField(
        blank = True,
        default = None,
        help_text = 'JSON Object After Change',
        null = True,
        verbose_name = 'After'
    )


    action = models.IntegerField(
        blank = False,
        choices=Actions,
        default=None,
        help_text = 'History action performed',
        null=True,
        verbose_name = 'Action'
    )


    user = models.ForeignKey(
        User,
        blank= False,
        help_text = 'User whom performed the action this history relates to',
        null = True,
        on_delete=models.DO_NOTHING,
        verbose_name = 'User'
    )

    content_type = models.ForeignKey(
        ContentType,
        blank= True,
        help_text = 'Model this note is for',
        null = False,
        on_delete=models.CASCADE,
        verbose_name = 'Content Model'
    )

    created = AutoCreatedField()



    child_history_models = []
    """Child History Models

    This list is currently used for excluding child models from the the history
    select_related query.

    Returns:
        list: Child history models.
    """


    table_fields: list  = [
        'created',
        'action',
        'content_type',
        'user',
        'nbsp',
        [
            'before',
            'after'
        ]
    ]


    def get_serialized_model_field(self, context):

        model = None

        model = getattr(self, self._meta.related_objects[0].name).model

        model = model.get_serialized_model(context).data

        return model


    def get_serialized_child_model_field(self, context):

        model = {}

        parent_model = getattr(self, self._meta.related_objects[0].name)

        child_model = getattr(parent_model, parent_model._meta.related_objects[0].name, None)

        if child_model is not None:

            model = child_model.get_serialized_child_model(context).data

        return model


    def get_url_kwargs(self) -> dict:

        parent_model = getattr(self, self._meta.related_objects[0].name)

        return {
            'model_class': parent_model.model._meta.model_name,
            'model_id': parent_model.model.pk,
            'pk': parent_model.pk
        }


    def get_url( self, request = None ) -> str:

        if request:

            return reverse(f"v2:_api_v2_model_history-detail", request=request, kwargs = self.get_url_kwargs() )

        return reverse(f"v2:_api_v2_model_history-detail", kwargs = self.get_url_kwargs() )
