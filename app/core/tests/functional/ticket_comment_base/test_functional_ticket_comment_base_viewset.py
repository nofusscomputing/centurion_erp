
import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.viewsets.ticket_comment import (
    ViewSet,
)



@pytest.mark.model_ticketcommentbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



    def test_function_get_queryset_filtered_results_action_list(self,
        viewset_mock_request, organization_one, organization_two, model
    ):

        viewset = viewset_mock_request

        viewset.action = 'list'

        if not viewset.model:
            pytest.xfail( reason = 'no model exists, assuming viewset is a base/mixin viewset.' )

        only_user_results_returned = True

        queryset = viewset.get_queryset()

        objects = model.objects.all()

        assert len( objects ) >= 2, 'multiple objects must exist for test to work'
        assert len( queryset ) > 0, 'Empty queryset returned. Test not possible'
        if model._meta.model_name != 'tenant':
            assert len(model.objects.filter( organization = organization_one)) > 0, 'objects in user org required for test to work.'
            objects[1].ticket.organization = organization_two
            objects[1].ticket.save()
            objects[1].save()
            assert len(model.objects.filter( organization = organization_two)) > 0, 'objects in different org required for test to work.'


        for result in queryset:

            if result.get_tenant() != organization_one:
                only_user_results_returned = False

        assert only_user_results_returned



class TicketCommentBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentBaseViewsetPyTest(
    ViewsetTestCases,
):


    @pytest.mark.xfail( reason = 'Action comments are excluded as user should not create via api.' )
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



    @pytest.mark.xfail( reason = 'Action comments are excluded as user should not create via api.' )
    def test_function_get_meta_urls_sub_models_values(self,
        viewset_mock_request, model
    ):
        """Test function `get_meta_urls`

        Ensure that the `sub_models` key values contain the correct url for 
        each of the sub_models.
        """


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

