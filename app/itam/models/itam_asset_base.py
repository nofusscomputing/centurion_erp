from django.apps import apps
from django.db import models

from accounting.models.asset_base import AssetBase



class ITAMAssetBase(
    AssetBase,
):
    """IT Asset Base Model

    This model forms the base of ALL IT asset models and contains the core
    features for all sub-models.

    **Don't** use this model directly, it should be used via a sub-model.
    """


    app_namespace = ''

    class Meta:

        ordering = [
            'id'
        ]

        sub_model_type = 'it_asset'

        itam_sub_model_type = 'itam_base'

        verbose_name = "IT Asset"

        verbose_name_plural = "IT Assets"



    @property
    def get_itam_model_type(self):
        """Fetch the ITAM Asset Type

        Returns:
            str: The models `Meta.m` in lowercase and without spaces
            None: The ticket is for the Base class. Used to prevent creating a base ticket.
        """

        model_type = str(self._meta.itam_sub_model_type).lower().replace(' ', '_')

        if model_type == 'itam_base':

            return None

        return model_type


    def get_itam_model_type_choices():

        choices = []

        if apps.ready:

            all_models = apps.get_models()

            for model in all_models:

                if(
                    ( isinstance(model, ITAMAssetBase) or issubclass(model, ITAMAssetBase) )
                    and ITAMAssetBase._meta.itam_sub_model_type != 'itam_base'

                ):

                    choices += [ (model._meta.itam_sub_model_type, model._meta.verbose_name) ]


        return choices

    itam_type = models.CharField(
        blank = True,
        choices = get_itam_model_type_choices,
        default = Meta.itam_sub_model_type,
        help_text = 'IT Asset Type. (derived from IT asset model)',
        max_length = 30,
        null = False,
        verbose_name = 'IT Asset Type',
    )


    # this model uses a custom page layout
    page_layout: list = []

    table_fields: list = [
        'id',
        {
            "field": "display_name",
            "type": "link",
            "key": "_self"
        },
        'itam_type',
        'asset_number',
        'serial_number',
        'organization',
        'created'
    ]


    def __str__(self):

        return self._meta.verbose_name + ' - ' + self.asset_number


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        related_model = self.get_related_model()

        if related_model is None:

            related_model = self

        if self.itam_type != str(related_model._meta.itam_sub_model_type).lower().replace(' ', '_'):

            self.itam_type = str(related_model._meta.itam_sub_model_type).lower().replace(' ', '_')

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
