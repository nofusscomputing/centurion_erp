from django.contrib.auth.models import ContentType
from django.db import models

from access.managers.common import CommonManager



class TicketModelManager(
    CommonManager
):
    """TicketModel Object Manager

    This manager specifically caters for the Ticket Models.
    """

    _content_filter = []

    def get_content_filter(self) -> list[ int ]:

        if not self._content_filter:

            content_filter = models.Q()
            model_permissions = {}

            for sub_model in self.model._meta.get_fields():

                model = sub_model.related_model

                if not model:
                    continue

                if not issubclass(model, self.model):
                    continue


                model_name = model._meta.model_name

                model_permissions.update({
                    f'{model._meta.app_label}.view_{model_name}': ContentType.objects.get_for_model(model).id
                })


            if len(model_permissions) == 0:

                model_permissions.update({
                    f'{self.model.model.field.model._meta.app_label}.view_{self.model.model.field.model._meta.model_name}': ContentType.objects.get_for_model(self.model.model.field.related_model).id
                })



            for tenancy, permissions in self._user.get_permissions().items():

                for user_permission in permissions:

                    if 'view' not in user_permission:
                        continue

                    if user_permission in model_permissions:

                        content_filter |= models.Q(
                            content_type_id = model_permissions[user_permission],
                            organization_id = int(tenancy.split('_')[1])
                        )


            self._content_filter= content_filter


        return self._content_filter


    def get_queryset(self):
        """ Fetch the data

        Fetch the linked model<>tickets filtered to the view permissions that the user has.

        Returns:
            (queryset): **super user**: return unfiltered data.
            (queryset): **not super user**: return data from the stored unique organizations.
        """

        content_filter = None
        if self._user:
            content_filter = self.get_content_filter()

        fields = [
            'organization',
            'ticket'
        ]

        if self.model.model:
            fields += [ 'model' ]

        if getattr(self._user, 'id', None) and getattr(self._user, 'is_authenticated', False):

            if not self._user.is_superuser and content_filter:

                return super().get_queryset().select_related( *fields ).filter(
                    content_filter
                )

            elif not content_filter:

                return super().get_queryset().none()



        if content_filter:
            return super().get_queryset().select_related( *fields )


        return super().get_queryset()
