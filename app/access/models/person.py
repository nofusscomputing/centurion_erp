from django.db import models

from core.exceptions import ValidationError

from access.models.entity import Entity



class Person(
    Entity
):


    class Meta:

        ordering = [
            'l_name',
            'm_name',
            'f_name',
            'dob',
        ]

        sub_model_type = 'person'

        verbose_name = 'Person'

        verbose_name_plural = 'People'

    f_name = models.CharField(
        blank = False,
        help_text = 'The persons first name',
        max_length = 64,
        unique = False,
        verbose_name = 'First Name'
    )

    m_name = models.CharField(
        blank = True,
        help_text = 'The persons middle name(s)',
        max_length = 100,
        null = True,
        unique = False,
        verbose_name = 'Middle Name(s)'
    )

    l_name = models.CharField(
        blank = False,
        help_text = 'The persons Last name',
        max_length = 64,
        unique = False,
        verbose_name = 'Last Name'
    )

    dob = models.DateField(
        blank = True,
        help_text = 'The Persons Date of Birth (DOB)',
        null = True,
        unique = False,
        verbose_name = 'DOB',
    )

    def __str__(self) -> str:

        return self.f_name + ' ' + self.l_name + f' (DOB: {self.dob})'

    documentation = ''

    history_model_name = 'person'

    page_layout: dict = []

    table_fields: list = [
        'organization',
        'f_name',
        'l_name',
        'dob',
        'created',
    ]


    def clean(self):

        super().clean()

        if self.dob is not None:

            if self.pk:

                duplicate_entry = Person.objects.filter(
                    f_name = self.f_name,
                    l_name = self.l_name,
                ).exclude(
                    pk = self.pk
                )

            else:

                duplicate_entry = Person.objects.filter(
                    f_name = self.f_name,
                    l_name = self.l_name,
                )


            for entry in duplicate_entry:
                    
                if(
                    entry.f_name == self.f_name
                    and entry.m_name == self.m_name
                    and entry.l_name == self.l_name
                    and entry.dob == self.dob
                ):

                    raise ValidationError(
                        detail = {
                            'dob': f'Person {self.f_name} {self.l_name} already exists with this birthday {entry.dob}'
                        },
                        code = 'duplicate_person_on_dob'
                    )

