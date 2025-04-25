from django.db import models

from access.models.person import Person



class Contact(
    Person
):


    class Meta:

        ordering = [
            'email',
        ]

        sub_model_type = 'contact'

        verbose_name = 'Contact'

        verbose_name_plural = 'Contacts'


    directory = models.BooleanField(
        blank = True,
        default = True,
        help_text = 'Show contact details in directory',
        null = False,
        verbose_name = 'Show in Directory',
    )

    email = models.EmailField(
        blank = False,
        help_text = 'E-mail address for this person',
        unique = True,
        verbose_name = 'E-Mail',
    )


    def __str__(self) -> str:

        return self.f_name + ' ' + self.l_name

    documentation = ''

    history_model_name = 'contact'

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                        'directory',
                    ]
                },
                {
                    "name": "Personal Details",
                    "layout": "double",
                    "left": [
                        'display_name',
                        'dob',
                    ],
                    "right": [
                        'f_name',
                        'm_name',
                        'l_name',
                    ]
                },
                {
                    "name": "",
                    "layout": "double",
                    "left": [
                        'email',
                    ],
                    "right": [
                        '',
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
        {
            "field": "display_name",
            "type": "link",
            "key": "_self"
        },
        'f_name',
        'l_name',
        'email',
        'organization',
        'created',
    ]
