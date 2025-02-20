from django.contrib.auth.models import ContentType

from access.models.organization import Organization



class HistoryEntriesCommon:
    """History Model Functional checks (ALL History Models)
    
    
        self.obj = self.model.objects.create(
            organization = self.organization,
            name = 'original_name'
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            name = 'delete_object_name'
        )


        self.call_the_banners()

    """

    model = None
    """ Model class to be tested"""

    history_model = None
    """ History Model class to be tested"""

    field_name = 'name'
    """Name of the field that will be checked within the audit model"""

    field_value_original = 'original_name'
    """Value of the field when creating the audit model"""

    field_value_changed = 'changed_name'
    """Value of the field when editing the audit model"""

    field_value_delete = 'delete_object_name'
    """Value of the field that is used for the audit model that will be deleted"""


    @classmethod
    def setUpTestData(self):

        self.organization = Organization.objects.create(name='test_org')

        self.extra_organization = Organization.objects.create(name='test_org_extra')


    @classmethod
    def call_the_banners(self):
        """User has setup object

        Run other actions required for test setup
        """

        setattr(self.obj, self.field_name, self.field_value_changed)

        self.obj.save()

        self.content_type = ContentType.objects.get(
            app_label = self.obj._meta.app_label,
            model = self.obj._meta.model_name,
        )

        if getattr(self, 'child_model', None):

            if self.field_value_child is None:

                print('you must set `self.field_value_child`')

                assert False

            self.history_entries_child = self.history_model_child.objects.all()

        self.history_entries = self.history_model.objects.all()




    def test_model_history_entry_create(self):
        """ Test model to ensure history entries are made

        On object create a history entry with action `ADD` must be created.
        """

        entries = self.history_entries.filter(
            model = self.obj,
            content_type = self.content_type,
            action = self.history_model.Actions.ADD
        )

        entry_exists = False

        for entry in entries:

            if entry.after.get(self.field_name, None):

                if entry.after[self.field_name] == self.field_value_original:

                    entry_exists = True
        
        assert entry_exists


    def test_model_history_entry_update(self):
        """ Test model to ensure history entries are made

        On object update a history entry with action `UPDATE` must be created.
        """

        entries = self.history_entries.filter(
            model = self.obj,
            content_type = self.content_type,
            action = self.history_model.Actions.UPDATE
        )

        entry_exists = False

        for entry in entries:

            if entry.after.get(self.field_name, None):

                if entry.after[self.field_name] == self.field_value_changed:

                    entry_exists = True
        
        assert entry_exists


    def test_model_history_entry_delete(self):
        """ Test model to ensure history entries are made

        On object delete all history entries must be removed
        """

        model_id = self.obj_delete.pk

        self.obj_delete.delete()

        entries = self.history_entries.filter(
            model_id = model_id,
            content_type = self.content_type,
        )

        entry_does_not_exists = True

        for entry in entries:

            if entry.after.get(self.field_name, None):

                if entry.after[self.field_name] == self.field_value_delete:

                    entry_does_not_exists = False
        
        assert entry_does_not_exists



class HistoryEntriesChildModel(
    HistoryEntriesCommon
):

    child_model = None
    """Child model class to be tested"""

    history_model_child = None
    """Child History Model class to be tested"""

    field_name_child = 'name'
    """Name of the field that will be checked within the audit model"""

    field_value_child = None
    """Value of the field when creating the audit model"""



    def test_model_history_entry_child_create(self):
        """ Test model to ensure history entries are made

        On object create a history entry with action `ADD` must be created.
        """

        entries = self.history_entries_child.filter(
            model = self.obj,
            child_model = self.obj_child,
            content_type = self.content_type,
            action = self.history_model.Actions.ADD
        )

        entry_exists = False

        for entry in entries:

            if entry.after.get(self.field_name_child, None):

                if entry.after[self.field_name_child] == self.field_value_child:

                    entry_exists = True
        
        assert entry_exists



    def test_model_history_entry_child_delete(self):
        """ Test model to ensure history entries are made

        On object delete a history entry with action `DELETE` must be created.
        """

        self.obj_child.delete()

        entries = self.history_entries_child.filter(
            model = self.obj,
            child_model = None,
            content_type = self.content_type,
            action = self.history_model.Actions.DELETE
        )

        entry_exists = False

        for entry in entries:

            if entry.before.get(self.field_name_child, None):

                if entry.before[self.field_name_child] == self.field_value_child:

                    entry_exists = True
        
        assert entry_exists
