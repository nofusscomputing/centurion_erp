import pytest

from django.test import TestCase

from core.tests.abstract.test_notes_viewset import NoteViewSetCommon

from core.models.notes import Notes

from itam.models.operating_system import OperatingSystem



class OperatingSystemNotePermissionsAPI(
    NoteViewSetCommon,
    TestCase,
):

    app_namespace = 'API'
    
    url_name = '_api_v2_operating_system_notes'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        super().setUpTestData()



        self.note_item = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'history-device'
        )

        self.note_item_b = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'history-device-b'
        )

        self.item = Notes.objects.create(
            organization = self.organization,
            note = 'a note',
            usercreated = self.view_user,
            operatingsystem = self.note_item
        )

        self.other_org_item = Notes.objects.create(
            organization = self.different_organization,
            note = 'b note',
            usercreated = self.view_user,
            operatingsystem = self.note_item_b
        )


        self.url_kwargs = {'operating_system_id': self.note_item.id}

        self.url_view_kwargs = {'operating_system_id': self.note_item.id, 'pk': self.item.pk }

        self.add_data = {'note': 'a note added', 'organization': self.organization.id}
