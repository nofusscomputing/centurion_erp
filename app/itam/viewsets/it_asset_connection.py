from .it_asset_related import ViewSet as RelatedViewSet



class ViewSet( RelatedViewSet ):
    """ M2M viewset

    This ViewSet is not documented (drf spectacular) as it will have the same
    URL signature as parent ViewSet.
    """


    def get_back_url(self) -> str:

        if self.kwargs.get(self.parent_model_pk_kwarg, None):

            return self.get_parent_model().objects.get(
                pk = int(self.kwargs[self.parent_model_pk_kwarg])
            ).get_url()


    def get_queryset(self):

        if not self._queryset:

            self._queryset = super().get_queryset()

            if self.kwargs['model_name'] == 'itassetmodel':

                self._queryset = self._queryset.filter( parent = None )


        return self._queryset
