
import pytest

from django.apps import apps

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.viewsets.ticket import (
    ViewSet,
)



@pytest.mark.model_ticketbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @pytest.mark.skip( reason = 'To be written.' )
    def test_permission_triage_task_comment_create(self):
        """Ticket Permission Check
        
        Only a user with permission `triage` on the ticket being edited
        can `create` a ticket task comment
        """
        pass


    @pytest.mark.skip( reason = 'To be written.' )
    def test_permission_triage_task_comment_edit(self):
        """Ticket Permission Check
        
        Only a user with permission `triage` on the ticket being edited
        can `create` a ticket task comment
        """
        pass


    @pytest.mark.skip( reason = 'To be written.' )
    def test_permission_triage_task_comment_delete(self):
        """Ticket Permission Check
        
        Only a user with permission `triage` on the ticket being edited
        can `create` a ticket task comment
        """
        pass


    @pytest.mark.xfail( reason = 'Project task ticket is a sub-model for use with project.' )
    def test_function_get_meta_urls_sub_models_keys(self,
        viewset_mock_request, model,
    ):
        """Test function `get_meta_urls`

        Ensure that the `sub_models` keys contain all of the models when the
        model tested is the base_model.
        """


        if model != model()._base_model:
            pytest.xfail( reason = 'model is not a base model, Test is N/A.' )


        urls = viewset_mock_request.get_meta_urls()

        sub_models: list = []

        for sub_model in apps.get_models():

            if issubclass(sub_model, model) and sub_model != model:
                sub_models.append(sub_model)


        assert 'sub_models' in urls, 'Missing sub-models key. test cant continue'


        assert sorted(
            [ key for key, value in urls['sub_models'].items() ]
        ) == sorted(
            [ sub_model._meta.model_name for sub_model in sub_models ]
        )


    def test_function_get_meta_urls_sub_models_keys_no_project_task(self,
        viewset_mock_request, model,
    ):
        """Test function `get_meta_urls`

        Ensure that the `sub_models` keys contain all of the models when the
        model tested is the base_model.
        """


        if model != model()._base_model:
            pytest.xfail( reason = 'model is not a base model, Test is N/A.' )


        urls = viewset_mock_request.get_meta_urls()

        sub_models: list = []

        for sub_model in apps.get_models():

            if(
                issubclass(sub_model, model)
                and sub_model != model
                and sub_model._meta.model_name != 'projecttaskticket'
            ):
                sub_models.append(sub_model)


        assert 'sub_models' in urls, 'Missing sub-models key. test cant continue'


        assert sorted(
            [ key for key, value in urls['sub_models'].items() ]
        ) == sorted(
            [ sub_model._meta.model_name for sub_model in sub_models ]
        )


    @pytest.mark.xfail( reason = 'Project task ticket is a sub-model for use with project.' )
    def test_function_get_meta_urls_sub_models_values(self,
        viewset_mock_request, model
    ):

        if model != model()._base_model:
            pytest.xfail( reason = 'model is not a base model' )

        urls = viewset_mock_request.get_meta_urls()

        sub_models: list = []

        for sub_model in apps.get_models():

            if issubclass(sub_model, model) and sub_model != model:
                sub_models.append(sub_model)


        assert 'sub_models' in urls, 'Missing sub-models key. test cant continue'


        assert sorted(
            [ value['url'] for key, value in urls['sub_models'].items() ]
        ) == sorted(
            [
                sub_model(
                    **viewset_mock_request.kwargs
                ).get_url(many = True) for sub_model in sub_models
            ]
        )


    def test_function_get_meta_urls_sub_models_values_no_project_task(self,
        viewset_mock_request, model
    ):
        """Test case overide of `test_function_get_meta_urls_sub_models_values`

        The sub-models for meta_urls must not include `projecttaskticket` as
        that model is a sub-model for use with projects only. hence require a
        project to exist to create the ticket type.
        """

        if model != model()._base_model:
            pytest.xfail( reason = 'model is not a base model' )

        urls = viewset_mock_request.get_meta_urls()

        sub_models: list = []

        for sub_model in apps.get_models():

            if(
                issubclass(sub_model, model)
                and sub_model != model
                and sub_model._meta.model_name != 'projecttaskticket'
            ):
                sub_models.append(sub_model)


        assert 'sub_models' in urls, 'Missing sub-models key. test cant continue'


        assert sorted(
            [ value['url'] for key, value in urls['sub_models'].items() ]
        ) == sorted(
            [
                sub_model(
                    **viewset_mock_request.kwargs
                ).get_url(many = True) for sub_model in sub_models
            ]
        )


class TicketBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
