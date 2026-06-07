import pytest

from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

from centurion.tests.integration.test_integration_common import (
    IntegrationCommon
)

from core.mixins.centurion import Centurion
from core.models.model_tickets import ModelTicketMetaModel



@pytest.mark.api
@pytest.mark.models
class ModelTestCases(
    IntegrationCommon
):


    def test_backend_crud_create(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be created.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        model_relative_url = the_model.get_url( many = True )

        the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['add'],
            json = kwargs_create,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "POST",
            url = url,
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



    def test_backend_crud_change(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be updated.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        model_relative_url = change_item.get_url( many = False )


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        change_data = {}

        for key, value in model_kwargs().items():

            if(
                key in ['name', 'title', 'model_notes']
                and value not in [ None, '']
            ):

                change_data[key] = value

                break

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['change'],
            json = change_data,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "PATCH",
            url = url,
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_backend_crud_delete(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be deleted.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = delete_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['delete'],
            method = "DELETE",
            url = url,
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content



    def test_backend_crud_view(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be viewed.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = view_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['view'],
            method = "GET",
            url = url,
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    @pytest.mark.parametrize(
        argnames = "url_many",
        argvalues = [ True, False ],
        ids = [ 'list_view', 'detail_view'],
    )
    def test_backend_view_metdata(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs, url_many
    ):
        """ Check Backend API 

        Ensure that the metadat for a model can be viewed.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        model_relative_url = view_item.get_url( many = url_many )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['view'],
            method = "GET",
            url = url,
        )

        assert response.status_code == 200, response.content



class AuditModelTestCases:
    """ Test Suite For Audit Models ONLY."""


    @pytest.fixture( scope = 'class' )
    def audit_model(self, request):

        yield request.cls.audit_model_class


    @pytest.fixture( scope = 'class', autouse = True)
    def model_kwargs(self, django_db_blocker,
        request, audit_model, kwargs_centurionauditmeta
    ):

        if not hasattr(request.cls, 'kwargs_create_item'):
            request.cls.kwargs_create_item = {}

        model_objs = []
        def factory(model_objs = model_objs):

            model_kwargs = kwargs_centurionauditmeta()

            with django_db_blocker.unblock():

                audit_model_kwargs = request.getfixturevalue('kwargs_' + audit_model._meta.model_name)()

                kwargs = {}

                many_field = {}

                for field, value in audit_model_kwargs.items():

                    if not hasattr(getattr(audit_model, field), 'field'):
                        continue

                    if isinstance(getattr(audit_model, field).field, models.ManyToManyField):

                        if field in many_field:

                            many_field[field] += [ value ]

                        elif isinstance(value, list):

                            value_list = []

                            for list_value in value:

                                value_list += [ list_value ]


                            value = value_list

                        else:

                            many_field.update({
                                field: [
                                    value
                                ]
                            })

                        continue

                    kwargs.update({
                        field: value
                    })


                model = audit_model.objects.create(
                    **kwargs
                )

                model_objs += [ model ]


                for field, values in many_field.items():

                    for value in values:

                        getattr(model, field).add( value )


            model_kwargs.update({
                'model': model
            })
            request.cls.kwargs_create_item.update({ **model_kwargs })

            return model_kwargs

        yield factory

        with django_db_blocker.unblock():

            for obj in model_objs:
                obj.delete()



    @pytest.fixture( scope = 'class' )
    def model(self, request):

        yield request.cls.model_class


    def test_backend_crud_create(self):
        pytest.xfail( reason = 'This model does not allow add by end user.' )



    def test_backend_crud_change(self):
        pytest.xfail( reason = 'This model does not allow change' )



    def test_backend_crud_delete(self):
        pytest.xfail( reason = 'This model does not allow removal' )




class CenturionModelNoteModelTestCases:
    """ Test Suite For Centurion Audit Note Models ONLY."""

    @pytest.fixture( scope = 'class' )
    def note_model(self, request):

        return request.cls.note_model_class


    @pytest.fixture( scope = 'class', autouse = True)
    def model_kwargs(self, django_db_blocker, clean_model_from_db,
        request, note_model, kwargs_centurionmodelnotemeta
    ):


        request.cls.kwargs_create_item = {}

        def factory(note_model = note_model,
            kwargs_centurionmodelnotemeta = kwargs_centurionmodelnotemeta,
        ):

            model_kwargs = kwargs_centurionmodelnotemeta()

            with django_db_blocker.unblock():

                note_model_kwargs = request.getfixturevalue('kwargs_' + note_model._meta.model_name)()

                kwargs = {}

                many_field = {}

                for field, value in note_model_kwargs.items():

                    if not hasattr(getattr(note_model, field), 'field'):
                        continue

                    if isinstance(getattr(note_model, field).field, models.ManyToManyField):

                        if field in many_field:

                            many_field[field] += [ value ]

                        elif isinstance(value, list):

                            value_list = []

                            for list_value in value:

                                value_list += [ list_value ]


                            value = value_list

                        else:

                            many_field.update({
                                field: [
                                    value
                                ]
                            })

                        continue

                    kwargs.update({
                        field: value
                    })


                model = note_model.objects.create(
                    **kwargs
                )

                for field, values in many_field.items():

                    for value in values:

                        getattr(model, field).add( value )


            model_kwargs.update({
                'model': model
            })
            request.cls.kwargs_create_item.update(model_kwargs)

            return model_kwargs

        yield factory

        clean_model_from_db(note_model)


    @pytest.fixture( scope = 'class' )
    def model(self, request, clean_model_from_db):

        yield request.cls.model_class

        clean_model_from_db(request.cls.model_class)


class ModelTicketMetaModelTestCases:


    @pytest.fixture( scope = 'class', autouse = True)
    def model_kwargs(self, django_db_blocker,
        request, kwargs_modelticketmetamodel, model_contenttype,
        model, organization_one
    ):

        model_objs = []
        def factory( model_objs = model_objs, model = model):

            model_kwargs = kwargs_modelticketmetamodel()

            with django_db_blocker.unblock():

                ticket_model_class =  apps.get_model(
                    app_label = model._meta.app_label,
                    model_name = str( model._meta.object_name )[0:len(model._meta.object_name)-6]
                )

                ticket_model = request.getfixturevalue(
                    # 'model_' + request.cls.ticket_model_class._meta.model_name
                    'model_' + ticket_model_class._meta.model_name
                )

                ticket_model_kwargs = request.getfixturevalue(
                    'kwargs_' + ticket_model._meta.model_name
                )()


                content_type = model_contenttype.objects.filter(
                    app_label = ticket_model._meta.app_label,
                    model = ticket_model._meta.model_name
                ).first()

                model_kwargs['content_type'] = content_type


                kwargs_many_to_many = {}

                kwargs = {}

                for key, value in ticket_model_kwargs.items():

                    field = ticket_model._meta.get_field(key)

                    if isinstance(field, models.ManyToManyField):

                        kwargs_many_to_many.update({
                            key: value
                        })

                    else:

                        kwargs.update({
                            key: value
                        })


                model = ticket_model.objects.create( **kwargs )

                model_objs += [ model ]

                for key, value in kwargs_many_to_many.items():

                    field = getattr(model, key)

                    for entry in value:

                        field.add(entry)


            if ticket_model_class._meta.model_name == 'tenant':
                model_kwargs['organization'] = organization_one
                model_kwargs['model'] = organization_one

            else:

                model_kwargs.update({
                    'model': model
                })

            request.cls.kwargs_create_item = model_kwargs

            return model_kwargs

        yield factory

        with django_db_blocker.unblock():

            for obj in model_objs:
                try:
                    obj.delete()
                except Exception:
                    pass


    def test_backend_crud_create(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be created.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        model_relative_url = the_model.get_url( many = True )

        the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id
        kwargs_create['model'] = the_model.model.id


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['add'],
            json = kwargs_create,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "POST",
            url = url,
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



def get_models( excludes: list[ str ] = [] ) -> list[ tuple ]:
    """Fetch models from Centurion Apps

    Args:
        excludes (list[ str ]): Words that may be in a models name to exclude

    Returns:
        list[ tuple ]: Centurion ERP Only models
    """

    models: list = []

    model_apps: list = []

    exclude_model_apps = [
        'django',
        'django_celery_results',
        'django_filters',
        'drf_spectacular',
        'drf_spectacular_sidecar',
        'coresheaders',
        'corsheaders',
        'rest_framework',
        'rest_framework_json_api',
        'social_django',
    ]

    for app in settings.INSTALLED_APPS:

        app = app.split('.')[0]

        if app in exclude_model_apps:
            continue

        model_apps += [ app ]


    for model in apps.get_models():

        model_name = str(model._meta.model_name)

        if model_name in excludes:
            continue

        models += [ model ]

    return models



def make_fixture_with_args(arg_names, func, decorator_factory=None, decorator_args=None):
    args_str = ", ".join(arg_names)

    src = f"""
@decorator_factory(**decorator_args)
def _generated(self, {args_str}):
    yield from func(self, {args_str})
"""

    local_ns = {}
    global_ns = {
        "func": func,
        "decorator_factory": decorator_factory,
        "decorator_args": decorator_args,
    }

    exec(src, global_ns, local_ns)
    return local_ns["_generated"]



def model_modelticket(self, model__model_name):

    yield self.test_model


def model(self, model__model_name, clean_model_from_db):

    yield model__model_name

    clean_model_from_db(model__model_name)



def model_kwargs(self, request, kwargs__model_name):

    kwargs = kwargs__model_name

    request.cls.kwargs_create_item = kwargs

    yield kwargs

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item



exclude_model_from_test = [
    'ConfigGroupHosts',    # No API Endpoint
]



class APIModelTestCases(
    ModelTestCases
):
    """API Model Test Cases

    This test suite is dynamically created for `Centurion` sub-classes.
    Each `Centurion` must ensure their model fixture exists in
    `tests/fixtures/model_<model_name>` with fixtures `model_<model_name>` and
    `kwargs_<model_name>` defined.
    """
    pass



for centurion_model in get_models(
                        excludes = [
                            'centurionmodelnote',    # Base Model
                            'centurionaudit',        # Base Model
                            'history',
                            'manufacturer',
                            'manufactureraudithistory',
                            'manufacturercenturionmodelnote',
                            'manufacturerticket',
                            'modelticket',
                            'notes'
                        ]
):

    if(
        not issubclass(centurion_model, Centurion)
        or centurion_model == Centurion
        or centurion_model._meta.object_name in exclude_model_from_test
    ):
        continue

    model_name = centurion_model._meta.model_name
    cls_name: str = f"{centurion_model._meta.object_name}APIModelPyTest"

    inc_classes = (APIModelTestCases,)
    try:

        additional_testcases = import_string(
            centurion_model._meta.app_label + '.tests.integration.additional_' +
            centurion_model._meta.model_name + '_model_endpoints.AdditionalTestCases'
        )

        inc_classes = (additional_testcases, *inc_classes)

    except Exception as ex:
        additional_testcases = None


    class_objects = {
        '__module__': 'api.tests.integration.test_integration_model_endpoints',
        '__qualname__': cls_name
    }


    if str('CenturionModelNote').lower() in model_name:

        class_objects['note_model_class'] = apps.get_model(
            app_label = centurion_model._meta.app_label,
            model_name = str( centurion_model._meta.object_name ).replace('CenturionModelNote', '')
        )

        class_objects['model_class'] = centurion_model

        inc_classes = ( CenturionModelNoteModelTestCases, ) + inc_classes

    elif str('AuditHistory').lower() in model_name:

        class_objects['audit_model_class'] = apps.get_model(
            app_label = centurion_model._meta.app_label,
            model_name = str( centurion_model._meta.object_name ).replace('AuditHistory', '')
        )
        class_objects['model_class'] = centurion_model

        inc_classes = ( AuditModelTestCases, ) + inc_classes

    elif(
        issubclass(centurion_model, ModelTicketMetaModel)
        and str(model_name).endswith( 'ticket' )
    ):

        class_objects['model'] = make_fixture_with_args(
            arg_names = [ 'model_modelticketmetamodel'  ],
            func = model_modelticket,
            decorator_factory = pytest.fixture,
            decorator_args = {'scope': 'class'}

        )

        class_objects['test_model'] = centurion_model

        inc_classes = ( ModelTicketMetaModelTestCases, ) + inc_classes

    else:

        class_objects['model'] = make_fixture_with_args(
            arg_names = [
                'model_' + str(centurion_model._meta.model_name),
                'clean_model_from_db'
            ],
            func = model,
            decorator_factory = pytest.fixture,
            decorator_args = {'scope': 'class'}

        )

        class_objects['model_kwargs'] = make_fixture_with_args(
            arg_names = ['request', f'kwargs_{model_name}' ],
            func = model_kwargs,
            decorator_factory = pytest.fixture,
            decorator_args = {'scope': 'class', 'autouse': True}
        )


    dynamic_class = type(
        cls_name,
        inc_classes,
        class_objects
    )

    model_mark = f"model_{str(model_name).replace('centurionmodelnote', '')}"
    dynamic_class = pytest.mark.__getattr__(model_mark)(dynamic_class)
    dynamic_class = pytest.mark.__getattr__('module_'+centurion_model._meta.app_label)(dynamic_class)

    globals()[cls_name] = dynamic_class
