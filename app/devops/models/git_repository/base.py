from django.db import models

from access.fields import AutoLastModifiedField

from core import exceptions as centurion_exceptions
from core.models.centurion import CenturionModel

from devops.models.git_group import GitGroup



class GitRepository(
    CenturionModel
):
    """Base Model for Git Repositories
    
    To Add a Git Repository, Create a new model ensuring it inherits from this
    model.
    """

    @property
    def _base_model(self):

        return GitRepository

    app_namespace = 'devops'

    documentation = ''

    model_tag = 'git_repository'

    url_model_name = 'gitrepository'


    class Meta:

        ordering = [
            'organization',
            'git_group',
            'path',
        ]

        # unique_together = [    # Cant use until import is a feature
        #     'provider',
        #     'provider_id',
        # ]

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

    provider = models.IntegerField(
        blank = False,
        choices = GitGroup.GitProvider,
        help_text = 'Who is the git Provider',
        null = False,
        verbose_name = 'Provider',
    )

    provider_id = models.IntegerField(
        blank = True,
        help_text = 'Providers ID for this repository',
        null = True,
        unique = False,
        verbose_name = 'Provider ID'
    )


    @property
    def provider_badge(self):

        from core.classes.badge import Badge

        text: str = self.get_provider_display()

        return Badge(
            icon_name = f'{text.lower()}',
            icon_style = f'badge-icon-action-{text.lower()}',
            text = text,
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
        unique = False,
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

    modified = AutoLastModifiedField()

    page_layout = []

    table_fields: list = [
        'name',
        'provider_badge',
        'path',
        'organization',
        'created',
    ]


    def __str__(self) -> str:

        return str(self.git_group) + '/' + self.path



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.organization = self.git_group.organization

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


    # def get_page_layout(self):

    #     return self.page_layout


    # def get_url_kwargs(self, many = False) -> dict:

    #     url_kwargs = super().get_url_kwargs()

    #     provider = ''

    #     if self.provider == GitGroup.GitProvider.GITHUB:

    #         provider = 'github'

    #     elif self.provider == GitGroup.GitProvider.GITLAB:

    #         provider = 'gitlab'

    #     url_kwargs.update({
    #         'git_provider': provider
    #     })

    #     return url_kwargs
