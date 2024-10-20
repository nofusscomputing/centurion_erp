from django.db import models

from access.fields import *
from access.models import TenancyObject


class ProjectCommonFields(TenancyObject):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField(
        editable = True,
    )

    modified = AutoLastModifiedField()



class ProjectCommonFieldsName(ProjectCommonFields):

    class Meta:
        abstract = True

    name = models.CharField(
        blank = False,
        max_length = 100,
        unique = True,
    )

    slug = AutoSlugField()
