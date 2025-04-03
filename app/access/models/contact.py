from django.db import models

from access.models.person import Person



class Contact(
    Person
):


    class Meta:

        ordering = [
            'email',
        ]

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

    page_layout: dict = []

    table_fields: list = [
        'organization',
        'f_name',
        'l_name',
        'created',
    ]
