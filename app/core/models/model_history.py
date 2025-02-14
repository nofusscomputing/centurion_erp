from django.contrib.auth.models import ContentType, User
from django.db import models

from access.fields import *


class ModelHistory(
    models.Model
):


    class Meta:

        ordering = [
            '-created'
        ]

        verbose_name = 'History'

        verbose_name_plural = 'History'


    class Actions(models.IntegerChoices):
        ADD    = 1, 'Create'
        UPDATE = 2, 'Update'
        DELETE = 3, 'Delete'


    id = models.AutoField(
        blank=False,
        help_text = 'ID for this history entry',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

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
