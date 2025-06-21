from django.apps import apps
from django.db import models

from rest_framework.reverse import reverse

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.tenancy import TenancyObject



class AssetBase(
    TenancyObject,
):
    """Asset Base Model

    This model forms the base of ALL asset models and contains the core
    features for all sub-models.

    **Don't** use this model directly, it should be used via a sub-model.
    """

    app_namespace = 'accounting'


    @property
    def _base_model(self):

        return AssetBase


    class Meta:

        ordering = [
            'id'
        ]

        sub_model_type = 'asset'

        verbose_name = "Asset"

        verbose_name_plural = "Assets"


    def validate_not_null(field):

        if field is None:

            return False

        return True



    is_global = None


    id = models.AutoField(
        blank = False,
        help_text = 'Ticket ID Number',
        primary_key = True,
        unique = True,
        verbose_name = 'Number',
    )

    asset_number = models.CharField(
        blank = True,
        help_text = 'Number or tag to use to track this asset',
        max_length = 30,
        null = True,
        unique = True,
        verbose_name = 'Asset Number',
    )

    serial_number = models.CharField(
        blank = True,
        help_text = 'Serial number of this asset assigned by manufacturer.',
        max_length = 30,
        null = True,
        unique = True,
        verbose_name = 'Serial Number',
    )


    # category = models.ForeignKey(
    #     TicketCategory,
    #     blank = False,
    #     help_text = 'Category for this asset',
    #     on_delete = models.PROTECT,
    #     verbose_name = 'Category',
    # )
    """Category & Subcategory: Assets are grouped into broad categories like IT
    equipment, vehicles, furniture, or heavy machinery, with further 
    subcategorization to increase granularity. This classification 
    facilitates reporting, lifecycle planning, and policy enforcement for 
    different asset types.
    """



    # Status

    # model (manufacturer / model)




    @property
    def get_model_type(self):
        """Fetch the Ticket Type

        You can safely override this function as long as it's called or the
        logic is included in your over-ridden function.

        Returns:
            str: The models `Meta.verbose_name` in lowercase and without spaces
            None: The ticket is for the Base class. Used to prevent creating a base ticket.
        """

        sub_model_type = str(self._meta.sub_model_type).lower().replace(' ', '_')

        if sub_model_type == 'asset':

            return None

        return sub_model_type


    def get_model_type_choices():

        choices = []

        if apps.ready:

            all_models = apps.get_models()

            for model in all_models:

                if(
                    ( isinstance(model, AssetBase) or issubclass(model, AssetBase) )
                    and AssetBase._meta.sub_model_type != 'asset'

                ):

                    choices += [ (model._meta.sub_model_type, model._meta.verbose_name) ]


        return choices

    asset_type = models.CharField(
        blank = True,
        choices = get_model_type_choices,
        default = Meta.sub_model_type,
        help_text = 'Asset Type. (derived from asset model)',
        max_length = 30,
        null = False,
        validators = [
            validate_not_null
        ],
        verbose_name = 'Asset Type',
    )



    created = AutoCreatedField(
        editable = True,
    )

    modified = AutoLastModifiedField()


    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'asset_type',
                        'asset_number',
                        'serial_number',
                    ],
                    "right": [
                        'model_notes',
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
            "name": "Tickets",
            "slug": "tickets",
            "sections": [
                {
                    "layout": "table",
                    "field": "tickets",
                }
            ],
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]

    table_fields: list = [
        'id',
        {
            "field": "display_name",
            "type": "link",
            "key": "_self"
        },
        'asset_type',
        'asset_number',
        'serial_number',
        'organization',
        'created'
    ]


    def __str__(self):

        return self.asset_type + ' - ' + self.asset_number



    def get_related_field_name(self) -> str:

        meta = getattr(self, '_meta')

        for related_object in getattr(meta, 'related_objects', []):

            if not issubclass(related_object.related_model, self._base_model):

                continue

            if getattr(self, related_object.name, None):

                if( 
                    not str(related_object.name).endswith('history')
                    and not str(related_object.name).endswith('notes')
                ):

                    return related_object.name


        return ''


    def get_related_model(self):
        """Recursive model Fetch

        Returns the lowest model found in a chain of inherited models.

        Args:
            model (models.Model, optional): Model to fetch the child model from. Defaults to None.

        Returns:
            models.Model: Lowset model found in inherited model chain
        """

        related_model_name = self.get_related_field_name()

        related_model = getattr(self, related_model_name, None)

        if related_model_name == '':

            related_model = None

        elif related_model is None:

            related_model = self

        elif hasattr(related_model, 'get_related_field_name'):

            if related_model.get_related_field_name() != '':

                related_model = related_model.get_related_model()


        return related_model




    def get_url( self, request = None ) -> str:

        kwargs = self.get_url_kwargs()

        url_path_name = '_api_v2_asset_sub'

        if self._meta.sub_model_type == 'asset':

            url_path_name = '_api_v2_asset'

        if request:

            return reverse(f"v2:accounting:{url_path_name}-detail", request=request, kwargs = kwargs )

        return reverse(f"v2:accounting:{url_path_name}-detail", kwargs = kwargs )



    def get_url_kwargs(self) -> dict:

        kwargs = {
            'asset_model': self.asset_type,
        }

        if self._meta.sub_model_type == 'asset':

            kwargs = {}


        if self.id:

            kwargs.update({
                'pk': self.id
            })

        return kwargs



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        related_model = self.get_related_model()

        if related_model is None:

            related_model = self

        if self.asset_type != str(related_model._meta.sub_model_type).lower().replace(' ', '_'):

            self.asset_type = str(related_model._meta.sub_model_type).lower().replace(' ', '_')

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)



    def save_history(self, before: dict, after: dict) -> bool:

        from accounting.models.asset_base_history import AssetBaseHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = AssetBaseHistory
        )


        return history
