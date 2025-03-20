from django.db import models

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.tenancy import TenancyObject

from core import exceptions as centurion_exceptions

from devops.models.git_group import GitGroup



class GitRepository(
    TenancyObject
):
    """Base Model for Git Repositories
    
    To Add a Git Repository, Create a new model ensuring it inherits from this
    model.
    """


    class Meta:

        ordering = [
            'organization',
            'git_group',
            'path',
        ]

        verbose_name = 'GIT Repository'

        verbose_name_plural = 'GIT Repositories'


    def validation_path(value):

        if '/' in value:

            raise centurion_exceptions.ValidationError(
                detail = {
                    'path': 'Path must not contain seperator `/`'
                },
                code = 'path_contains_separator'
            )

    is_global = None

    id = models.AutoField(
        blank = False,
        help_text = 'Primary key of the entry',
        primary_key = True,
        unique = True,
        verbose_name = 'ID'
    )

    provider = models.IntegerField(
        blank = False,
        choices = GitGroup.GitProvider,
        help_text = 'Who is the git Provider',
        null = False,
        verbose_name = 'Provider',
    )

    provider_id = models.IntegerField(
        blank = False,
        help_text = 'Providers ID for this repository',
        unique = True,
        verbose_name = 'Provider ID'
    )

    git_group = models.ForeignKey(
        GitGroup,
        blank = False,
        help_text = 'Git Group this repository belongs to.',
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Group',
    )

    path = models.CharField(
        blank = False,
        help_text = 'Path to this repository, not including the organization',
        max_length = 80,
        null = False,
        unique = True,
        validators = [ validation_path ],
        verbose_name = 'path'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the repository',
        max_length = 80,
        null = False,
        unique = False,
        verbose_name = 'Name'
    )

    description = models.TextField(
        blank = True,
        help_text = 'Repository Description',
        max_length = 300,
        null = True,
        verbose_name = 'Description'
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def __str__(self) -> str:

        return str(self.git_group) + '/' + self.path

    app_namespace = 'devops'

    documentation = ''

    page_layout: dict = []


    table_fields: list = [
        'name',
        'provider',
        'path',
        'organization',
        'created',
    ]
