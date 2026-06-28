import pytest

from django.db import models

from core.tests.unit.ticket_base.test_unit_ticket_base_model import TicketBaseModelInheritedCases

from project_management.models.ticket_project_task import ProjectTaskTicket



@pytest.mark.model_projecttaskticket
class ProjectTaskTicketModelTestCases(
    TicketBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'url_model_name': {
                'type': str,
                'value': 'project_ticket'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {}



    def test_class_inherits_ProjectTaskTicket(self, model):
        """ Class inheritence

        Model Must Inherit from projecttaskticket
        """

        assert issubclass(model, ProjectTaskTicket)



    def test_method_get_url_kwargs(self, model_instance):

        assert model_instance.get_url_kwargs() == {
            'project_id': model_instance.project.id,
            'model_name': model_instance._meta.model_name,
            'pk': model_instance.id
        }


    def test_method_get_url_attribute__is_submodel_set(self, mocker, model_instance, settings):

        site_path = '/module/page/1'

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = site_path)


        model_instance.model = model_instance

        app_namespace = ''
        if model_instance.app_namespace:
            app_namespace = model_instance.app_namespace + ':'

        url_model_name = model_instance._meta.model_name
        if model_instance.url_model_name:
            url_model_name = model_instance.url_model_name

        url_basename = f'v2:{app_namespace}_api_{url_model_name}-detail'
        if model_instance._meta.model_name != 'ticketbase':
            url_basename = f'v2:{app_namespace}_api_{url_model_name}_sub-detail'

        url = model_instance.get_url( relative = True)

        reverse.assert_called_with(
            url_basename,
            None,
            {
                'project_id': model_instance.project.id,
                'model_name': model_instance._meta.model_name,
                'pk': model_instance.id,
            },
            None,
            None
        )



class ProjectTaskTicketModelInheritedCases(
    ProjectTaskTicketModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectTaskTicketModelPyTest(
    ProjectTaskTicketModelTestCases,
):
    pass
