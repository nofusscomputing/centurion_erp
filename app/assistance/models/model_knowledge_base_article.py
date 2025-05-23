import importlib

from django.apps import apps
from django.db import models

from access.fields import *
from access.models.tenancy import TenancyObject

from assistance.models.knowledge_base import KnowledgeBase

from core.lib.feature_not_used import FeatureNotUsed


def all_models() -> list(tuple()):

    models: list(tuple()) = []

    model_apps: list = [
        'access',
        'accounting',
        'api',
        'app',
        'assistance',
        'config_management',
        'core',
        'devops',
        'human_resources',
        'itam',
        'itim',
        'project_management',
        'settings',
    ]

    excluded_models: list = [
        'appsettings',
        'authtoken',
        'configgrouphosts',
        'configgroupsoftware',
        'deviceoperatingsystem',
        'devicesoftware',
        'history',
        'knowledgebase',
        'modelknowledgebasearticle',
        'notes',
        'relatedtickets',
        'teamusers',
        'ticket',
        'ticketcomment',
        'ticketlinkeditem',
        'token',
        'usersettings',
    ]

    for app_model in apps.get_models():

        if(
            str(app_model._meta.app_label) in model_apps
            and str(app_model._meta.model_name) not in excluded_models
            and not str(app_model._meta.model_name).lower().endswith('notes')
        ):

            models.append(
                (str(app_model._meta.app_label) + '.' + str(app_model._meta.model_name), str(app_model._meta.verbose_name))
            )

        models.sort(key=lambda tup: tup[1])

    return models


class ModelKnowledgeBaseArticle(TenancyObject):


    class Meta:

        default_permissions = ('add', 'delete', 'view')

        ordering = [
            'model',
            'id'
        ]

        unique_together = ('article', 'model', 'model_pk',)

        verbose_name = "Model Knowledge Base Article"

        verbose_name_plural = "Model Knowledge Base Articles"


    model_notes = None


    id = models.AutoField(
        blank=False,
        help_text = 'ID of this KB article link',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )


    article = models.ForeignKey(
        KnowledgeBase,
        blank = False,
        help_text = 'Article to be linked to model',
        null = False,
        on_delete = models.CASCADE,
        unique = False,
        verbose_name = 'Article',
    )


    model = models.CharField(
        blank = False,
        choices = all_models,
        help_text = 'Model type to link to article article',
        max_length = 50,
        null = False,
        unique = False,
        verbose_name = 'Model Type',
    )


    model_pk = models.IntegerField(
        blank = False,
        help_text = 'PK of the model the article is linked to',
        null = False,
        unique = False,
        verbose_name = 'Model Primary Key'
    )


    created = AutoCreatedField()


    modified = AutoLastModifiedField()


    page_layout: list = []

    table_fields: list = [
        'article',
        'category',
        'organization',
        'created',
        'modified',
    ]


    def clean(self):

        for model in apps.get_models():

            if(
                str(model._meta.app_label) + '.' + str(model._meta.model_name)
                ==
                self.model
            ):

                app = importlib.import_module( model.__module__ )

                model_class = getattr(app, model.__name__)

                item = model_class.objects.get(pk = self.model_pk)

                if item:

                    self.organization = item.organization


    def get_url( self, request = None ):
        """ Function not required nor-used"""

        return None

    def get_url_kwargs_notes(self):

        return FeatureNotUsed
