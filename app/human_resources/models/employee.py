from django.db import models

from access.models.contact import Contact



class Employee(
    Contact
):

    documentation = ''

    _is_submodel = True


    class Meta:

        ordering = [
            'email',
        ]

        sub_model_type = 'employee'

        verbose_name = 'Employee'

        verbose_name_plural = 'Employees'


    employee_number = models.IntegerField(
        blank = False,
        help_text = 'Employees identification number.',
        null = False,
        unique = True,
        verbose_name = 'Employee Number'
    )


    def __str__(self) -> str:

        return self.f_name + ' ' + self.l_name

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
                    "name": "Contact Details",
                    "layout": "double",
                    "left": [
                        'email',
                    ],
                    "right": [
                        '',
                    ]
                },
                {
                    "name": "Employee Details",
                    "layout": "double",
                    "left": [
                        'employee_number',
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
            "field": "employee_number",
            "type": "link",
            "key": "_self"
        },
        'f_name',
        'l_name',
        'email',
        'organization',
        'created',
    ]
