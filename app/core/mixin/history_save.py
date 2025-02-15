import json

from django.contrib.auth.models import ContentType
from django.db import models

from core.middleware.get_request import get_request



class SaveHistory(models.Model):

    save_model_history: bool = True
    """When set, history will be saved.
    By default, ALL models must save history.
    """

    class Meta:
        abstract = True


    @property
    def fields(self):
        return [ f.name for f in self._meta.fields + self._meta.many_to_many ]


    def save_history(self, before: dict, after: dict, history_model = None) -> bool:
        """Save Model History

        This method must be re-implemented by the model class in question so
        that the history model can be passed to this function.

        Args:
            before (dict): Model data before the change
            after (dict): Model data after the change
            history_model (models.Model): History model class

        Returns:
            False (bool): Failed to save history
            True (bool): Successfully saved history
            None (None): history_model was not specified
        """

        if history_model is None:

            return None


        remove_keys = [
            '_django_version',
            '_state',
            'created',
            'modified'
        ]


        from core.models.model_history import ModelHistory

        clean = {}
        for entry in before:

            if type(before[entry]) == type(int()):

                value = int(before[entry])

            elif type(before[entry]) == type(bool()):

                value = bool(before[entry])

            elif (
                    "{" in str(after[entry]) 
                        and
                    "}" in str(after[entry])
                ) or (
                    "[" in str(after[entry])
                        and
                    "]" in str(after[entry])
                ):

                value = str(after[entry]).replace("'", '\"')

            else:

                value = str(before[entry])


            if entry not in remove_keys:
                clean[entry] = value

        before_json = clean

        clean = {}
        for entry in after:

            if type(after[entry]) == type(int()):

                value = int(after[entry])

            elif type(after[entry]) == type(bool()):

                value = bool(after[entry])

            elif (
                    "{" in str(after[entry]) 
                        and
                    "}" in str(after[entry])
                ) or (
                    "[" in str(after[entry])
                        and
                    "]" in str(after[entry])
                ):

                value = str(after[entry]).replace("'", '\"')

            else:

                value = str(after[entry])


            if entry not in remove_keys and str(before) != '{}':

                if after[entry] != before[entry]:
                    clean[entry] = value

            elif entry not in remove_keys:

                clean[entry] = value


        after_json = clean

        audit_model = self
        parent_model = None

        if getattr(self, 'parent_object', None):

            parent_model = self.parent_object


        action = ModelHistory.Actions.UPDATE

        if not before:

            action = ModelHistory.Actions.ADD

        elif self.pk is None:

            action = ModelHistory.Actions.DELETE
            after_json = None


        current_user = None
        if get_request() is not None:

            current_user = get_request().user

            if current_user.is_anonymous:
                current_user = None


        if before_json != after_json:

            if parent_model is not None:

                entry = history_model.objects.create(
                    organization = self.organization,
                    before = before_json,
                    after = after_json,
                    action = action,
                    user = current_user,
                    content_type = ContentType.objects.get(
                        app_label= parent_model._meta.app_label,
                        model = parent_model._meta.model_name
                    ),
                    model = parent_model,
                    child_model = audit_model,
                )

            else:

                entry = history_model.objects.create(
                    organization = self.organization,
                    before = before_json,
                    after = after_json,
                    action = action,
                    user = current_user,
                    content_type = ContentType.objects.get(
                        app_label= audit_model._meta.app_label,
                        model = audit_model._meta.model_name
                    ),
                    model = audit_model,
                )

            entry.save()



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ OverRides save for keeping model history.

        Not a Full-Override as this is just to add to existing.

        Before to fetch from DB to ensure the changed value is the actual changed value and the after
        is the data that was saved to the DB.
        """

        before = {}

        try:
            before = self.__class__.objects.get(pk=self.pk).__dict__.copy()
        except Exception:
            pass

        # Process the save
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if self.save_model_history:

            after = self.__dict__.copy()

            self.save_history(before, after)
