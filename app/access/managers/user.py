from access.managers.common import CommonManager



class UserManager(
    CommonManager
):
    """Multi-Tennant Object Manager

    This manager specifically caters for the multi-tenancy features of Centurion ERP.
    """


    def get_queryset(self):
        """ Fetch the data

        It's assumed that the query method from the view/ViewSet has added the user object
        to the model under attribute `.context[<_meta.model_name>]` as that's the model the user is
        fetching for their query. It's done like this so that within code, a full query can
        be done without the data being filtered to the user in question.

        Returns:
            (queryset): **super user**: return unfiltered data.
            (queryset): **not super user**: return data from the stored unique organizations.
        """

        if getattr(self._user, 'id', None) and getattr(self._user, 'is_authenticated', False):

            return super().get_queryset().filter(
                user = self._user
            )


        return super().get_queryset()
