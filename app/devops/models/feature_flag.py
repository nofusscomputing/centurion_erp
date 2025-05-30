from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel

from itam.models.software import Software



class FeatureFlag(
    CenturionModel
):


    app_namespace = 'devops'

    documentation = 'devops/feature_flags'

    model_tag = 'feature_flag'


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Feature Flag'

        verbose_name_plural = 'Feature Flag'


    software = models.ForeignKey(
        Software,
        blank = False,
        help_text = 'Software this feature flag is for',
        # limit_choices_to = {    # bug: returns duplicates
        #     'feature_flagging__enabled': True
        # },
        on_delete = models.PROTECT,
        related_name = 'feature_flags',
        verbose_name = 'Software',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this feature',
        max_length = 50,
        unique = False,
        verbose_name = 'Name'
    )

    description = models.TextField(
        blank = True,
        help_text = 'Description of this feature',
        max_length = 300,
        null = True,
        unique = False,
        verbose_name = 'Description'
    )

    enabled = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this feature enabled',
        verbose_name = 'Enabled'
    )

    modified = AutoLastModifiedField()

    is_global = None    # Field not requied.


    def __str__(self) -> str:

        return self.name

    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'software',
                        'name',
                        'enabled',
                    ],
                    "right": [
                        'model_notes',
                        'description',
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
        },
    ]


    table_fields: list = [
        'name',
        'enabled',
        'software',
        'organization',
        'created',
        # 'modified'
    ]
