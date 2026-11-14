import pytest

from django.test import Client
from django.urls.exceptions import NoReverseMatch

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from api.tests.functional.test_functional_permissions_api import (
    APIPermissionAddInheritedCases,
    APIPermissionChangeInheritedCases,
    APIPermissionDeleteInheritedCases,
    APIPermissionViewInheritedCases,
)



class AdditionalTestCases:


    @pytest.fixture( scope = 'class')
    def api_request_permissions_m2m(self, api_request_permissions,
        django_db_blocker, model_kwargs, model_permission,
        model_contenttype,
    ):


        with django_db_blocker.unblock():

            amended_request_permissions = api_request_permissions.copy()

            kwargs = model_kwargs()

            parent_model = kwargs['parent_asset_model']

            change_permission = model_permission.objects.get(
                    codename = 'change_' + parent_model._meta.model_name,
                    content_type = model_contenttype.objects.get(
                        app_label = parent_model._meta.app_label,
                        model = parent_model._meta.model_name,
                    )
                )

            amended_request_permissions['user']['add'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            amended_request_permissions['user']['change'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            amended_request_permissions['user']['delete'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            view_permission = model_permission.objects.get(
                    codename = 'view_' + parent_model._meta.model_name,
                    content_type = model_contenttype.objects.get(
                        app_label = parent_model._meta.app_label,
                        model = parent_model._meta.model_name,
                    )
                )

            amended_request_permissions['user']['view'].groups.all(
            ).first().roles.all().first().permissions.add(view_permission)


        yield amended_request_permissions



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = APIPermissionAddInheritedCases.permission_no_add,
        ids=[test_name for test_name, user, expected in APIPermissionAddInheritedCases.permission_no_add]
    )
    def test_permission_no_add(
        self, model_kwargs, kwargs_api_create, model_instance,
        api_request_permissions, test_name, user, expected
    ):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        if hasattr(self, 'exclude_permission_no_add'):

            for name, reason in getattr(self, 'exclude_permission_no_add'):

                if name == test_name:

                    pytest.xfail( reason = reason )


        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        the_model = model_instance( kwargs_create = model_kwargs() )

        try:

            response = client.post(
                path = the_model.get_url( many = True ),
                data = kwargs_api_create
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.get(
                    path = the_model.get_url( many = False ),
                    data = kwargs_api_create
                )

            except NoReverseMatch:

                pass

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )


        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        # the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        # kwargs_create['model'] = the_model.model.id

        if kwargs.get('created_by', None ):

            kwargs_create['created_by'] = api_request_permissions['user']['add'].id

        if kwargs.get('organization', None ):

            kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        try:

            response = client.post(
                path = url,
                data = kwargs_create,
                content_type = 'application/json'
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.post(
                    path = the_model.get_url( many = False ),
                    data = kwargs_create
                )

            except NoReverseMatch:

                pass


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = APIPermissionChangeInheritedCases.permission_no_change,
        ids=[test_name for test_name, user, expected in APIPermissionChangeInheritedCases.permission_no_change]
    )
    def test_permission_no_change(self, model_instance, api_request_permissions, test_name, user, expected,
        model_kwargs
    ):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        if hasattr(self, 'exclude_permission_no_change'):

            for name, reason in getattr(self, 'exclude_permission_no_change'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()


        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })


        change_item = model_instance(
            kwargs_create = kwargs,
        )

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_permission_change(self, model_instance, api_request_permissions, model_kwargs):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = APIPermissionDeleteInheritedCases.permission_no_delete,
        ids=[test_name for test_name, user, expected in APIPermissionDeleteInheritedCases.permission_no_delete]
    )
    def test_permission_no_delete(self, model_instance, api_request_permissions,
        test_name, user, expected, model_kwargs
    ):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        if hasattr(self, 'exclude_permission_no_delete'):

            for name, reason in getattr(self, 'exclude_permission_no_delete'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_permission_delete(self, model_instance, api_request_permissions, model_kwargs):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = APIPermissionViewInheritedCases.permission_no_view,
        ids=[test_name for test_name, user, expected in APIPermissionViewInheritedCases.permission_no_view]
    )
    def test_permission_no_view(self, model_instance, api_request_permissions,
        test_name, user, expected, model_kwargs
    ):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        if hasattr(self, 'exclude_permission_no_view'):

            for name, reason in getattr(self, 'exclude_permission_no_view'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.get(
            path = view_item.get_url( many = False )
        )

        if response.status_code == 405:

            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable' )

        assert response.status_code == int(expected), response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_permission_view(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.get(
            path = view_item.get_url( many = False )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_permission_metdata(self, model_instance, api_request_permissions,
        model_kwargs
    ):
        """ Check correct permission for view metadata

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.options(
            path = view_item.get_url( many = False )
        )

        assert response.status_code == 200, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_returned_results_only_user_orgs(self, model_instance, model_kwargs, api_request_permissions):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        if model_kwargs().get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )


        client = Client()

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
        ]

        if getattr(self, 'global_organization', None):
            # Cater for above test that also has global org

            viewable_organizations += [ api_request_permissions['tenancy']['global'] ]


        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })

        model_instance(
            kwargs_create = kwargs
        )

        the_model = model_instance( kwargs_create = model_kwargs() )

        response = client.get(
            path = the_model.get_url( many = True )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )


        assert response.status_code == 200
        assert len(response.data['results']) > 0

        contains_different_org: bool = False

        for item in response.data['results']:

            if 'organization' not in item:
                pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

            if int(item['organization']['id']) == api_request_permissions['tenancy']['global'].id:
                continue

            if int(item['organization']['id']) not in viewable_organizations:

                contains_different_org = True
                print(f'Failed returned row was: {item}')

        assert not contains_different_org



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_returned_data_from_user_and_global_organizations_only(
        self, model, model_instance, model_kwargs, api_request_permissions
    ):
        """Check items returned

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        if model_kwargs().get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

        client = Client()

        only_from_user_org: bool = True

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
            api_request_permissions['tenancy']['global'].id
        ]


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })

        the_model1 = model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })

        the_model2 =model_instance(
            kwargs_create = kwargs
        )


        client.force_login( api_request_permissions['user']['view'] )

        the_model3 = model_instance( kwargs_create = model_kwargs() )

        response = client.get(
            path = the_model3.get_url( many = True )
        )

        if response.status_code == 405:

            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )

        assert response.status_code == 200, 'http success not returned, test cant continue.'
        assert len(model.objects.filter()) >= 2, 'multiple objects in multiple orgs must exist for test to continue.'


        for row in response.data['results']:

            if 'organization' not in row:
                pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

            if row['organization']['id'] not in viewable_organizations:

                only_from_user_org = False

                print(f"Users org: {api_request_permissions['tenancy']['user'].id}")
                print(f"global org: {api_request_permissions['tenancy']['global'].id}")
                print(f'Failed returned row was: {row}')

        assert only_from_user_org
        try:
            the_model1.delete()
        except:
            pass
        try:
            the_model2.delete()
        except:
            pass
        try:
            the_model3.delete()
        except:
            pass



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_api_add_exception(self, mocker, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs, kwargs_api_create, model
    ):
        """ API action capture exception

        Ensure that during a `Create` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        # the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        # kwargs_create['model'] = the_model.model.id
        kwargs_create['created_by'] = api_request_permissions['user']['add'].id
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id

        mocker.patch(
            f'{model.__module__}.{model.__name__}.objects.create',
            side_effect = param_exception("an integrity error occured....")
        )

        mocker.patch(
            "access.managers.tenancy.TenancyManager.create",
            side_effect = param_exception("an integrity error occured....")
        )


        try:

            response = client.post(
                path = url,
                data = kwargs_create,
                content_type = 'application/json'
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.post(
                    path = the_model.get_url( many = False ),
                    data = kwargs_create
                )

            except NoReverseMatch:

                pass


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_api_change_exception(self, mocker, model, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs
    ):
        """ API action capture exception

        Ensure that during a `Change` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        mocker.patch(
            f"{model.__module__}.{model.__name__}.save",
            side_effect = param_exception("an integrity error occured....")
        )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_api_delete_exception(self, mocker, model, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs
    ):
        """ API action capture exception

        Ensure that during a `Delete` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        mocker.patch(
            f"{model.__module__}.{model.__name__}.delete",
            side_effect = param_exception("an integrity error occured....")
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content























    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = APIPermissionAddInheritedCases.permission_no_add,
        ids=[test_name for test_name, user, expected in APIPermissionAddInheritedCases.permission_no_add]
    )
    def test_permission_no_add_m2m_model(
        self, model_kwargs, kwargs_api_create, model_instance,
        api_request_permissions_m2m, test_name, user, expected
    ):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        if hasattr(self, 'exclude_permission_no_add'):

            for name, reason in getattr(self, 'exclude_permission_no_add'):

                if name == test_name:

                    pytest.xfail( reason = reason )


        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions_m2m['user'][user] )

        the_model = model_instance( kwargs_create = model_kwargs() )

        try:

            response = client.post(
                path = the_model.get_url( many = True ),
                data = kwargs_api_create
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.get(
                    path = the_model.get_url( many = False ),
                    data = kwargs_api_create
                )

            except NoReverseMatch:

                pass

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    def test_permission_add_m2m_model(self, model_instance, api_request_permissions_m2m,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions_m2m['user']['add'] )


        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions_m2m['tenancy']['user']
            })

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        # the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        # kwargs_create['model'] = the_model.model.id

        if kwargs.get('created_by', None ):

            kwargs_create['created_by'] = api_request_permissions_m2m['user']['add'].id

        if kwargs.get('organization', None ):

            kwargs_create['organization'] = api_request_permissions_m2m['tenancy']['user'].id


        try:

            response = client.post(
                path = url,
                data = kwargs_create,
                content_type = 'application/json'
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.post(
                    path = the_model.get_url( many = False ),
                    data = kwargs_create
                )

            except NoReverseMatch:

                pass


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = APIPermissionChangeInheritedCases.permission_no_change,
        ids=[test_name for test_name, user, expected in APIPermissionChangeInheritedCases.permission_no_change]
    )
    def test_permission_no_change_m2m_model(self, model_instance, api_request_permissions_m2m, test_name, user, expected,
        model_kwargs
    ):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        if hasattr(self, 'exclude_permission_no_change'):

            for name, reason in getattr(self, 'exclude_permission_no_change'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()


        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions_m2m['tenancy']['user']
            })


        change_item = model_instance(
            kwargs_create = kwargs,
        )

        if user != 'anon':

            client.force_login( api_request_permissions_m2m['user'][user] )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    def test_permission_change_m2m_model(self, model_instance, api_request_permissions_m2m, model_kwargs):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        client.force_login( api_request_permissions_m2m['user']['change'] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions_m2m['tenancy']['user']
            })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = APIPermissionDeleteInheritedCases.permission_no_delete,
        ids=[test_name for test_name, user, expected in APIPermissionDeleteInheritedCases.permission_no_delete]
    )
    def test_permission_no_delete_m2m_model(self, model_instance, api_request_permissions_m2m,
        test_name, user, expected, model_kwargs
    ):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        if hasattr(self, 'exclude_permission_no_delete'):

            for name, reason in getattr(self, 'exclude_permission_no_delete'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions_m2m['user'][user] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions_m2m['tenancy']['user']
            })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    def test_permission_delete_m2m_model(self, model_instance, api_request_permissions_m2m, model_kwargs):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()

        client.force_login( api_request_permissions_m2m['user']['delete'] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions_m2m['tenancy']['user']
            })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content



    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = APIPermissionViewInheritedCases.permission_no_view,
        ids=[test_name for test_name, user, expected in APIPermissionViewInheritedCases.permission_no_view]
    )
    def test_permission_no_view_m2m_model(self, model_instance, api_request_permissions_m2m,
        test_name, user, expected, model_kwargs
    ):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        if hasattr(self, 'exclude_permission_no_view'):

            for name, reason in getattr(self, 'exclude_permission_no_view'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions_m2m['user'][user] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions_m2m['tenancy']['user']
            })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.get(
            path = view_item.get_url( many = False )
        )

        if response.status_code == 405:

            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable' )

        assert response.status_code == int(expected), response.content



    def test_permission_view_m2m_model(self, model_instance, api_request_permissions_m2m,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions_m2m['user']['view'] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions_m2m['tenancy']['user']
            })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.get(
            path = view_item.get_url( many = False )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_permission_metdata_m2m_model(self, model_instance, api_request_permissions_m2m,
        model_kwargs
    ):
        """ Check correct permission for view metadata

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions_m2m['user']['view'] )

        kwargs = model_kwargs()

        if kwargs.get('organization', None ):

            kwargs.update({
                'organization': api_request_permissions_m2m['tenancy']['user']
            })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.options(
            path = view_item.get_url( many = False )
        )

        assert response.status_code == 200, response.content



    def test_returned_results_only_user_orgs_m2m_model(self, model_instance, model_kwargs, api_request_permissions_m2m,):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        if model_kwargs().get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )


        client = Client()

        viewable_organizations = [
            api_request_permissions_m2m['tenancy']['user'].id,
        ]

        if getattr(self, 'global_organization', None):
            # Cater for above test that also has global org

            viewable_organizations += [ api_request_permissions_m2m['tenancy']['global'] ]


        client.force_login( api_request_permissions_m2m['user']['view'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['different']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['global']
        })

        model_instance(
            kwargs_create = kwargs
        )

        the_model = model_instance( kwargs_create = model_kwargs() )

        response = client.get(
            path = the_model.get_url( many = True )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )


        assert response.status_code == 200
        assert len(response.data['results']) > 0

        contains_different_org: bool = False

        for item in response.data['results']:

            if 'organization' not in item:
                pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

            if int(item['organization']['id']) == api_request_permissions_m2m['tenancy']['global'].id:
                continue

            if int(item['organization']['id']) not in viewable_organizations:

                contains_different_org = True
                print(f'Failed returned row was: {item}')

        assert not contains_different_org



    def test_returned_data_from_user_and_global_organizations_only_m2m_model(
        self, model, model_instance, model_kwargs, api_request_permissions_m2m,
    ):
        """Check items returned

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        if model_kwargs().get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

        client = Client()

        only_from_user_org: bool = True

        viewable_organizations = [
            api_request_permissions_m2m['tenancy']['user'].id,
            api_request_permissions_m2m['tenancy']['global'].id
        ]


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['different']
        })

        the_model1 = model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['global']
        })

        the_model2 =model_instance(
            kwargs_create = kwargs
        )


        client.force_login( api_request_permissions_m2m['user']['view'] )

        the_model3 = model_instance( kwargs_create = model_kwargs() )

        response = client.get(
            path = the_model3.get_url( many = True )
        )

        if response.status_code == 405:

            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )

        assert response.status_code == 200, 'http success not returned, test cant continue.'
        assert len(model.objects.filter()) >= 2, 'multiple objects in multiple orgs must exist for test to continue.'


        for row in response.data['results']:

            if 'organization' not in row:
                pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

            if row['organization']['id'] not in viewable_organizations:

                only_from_user_org = False

                print(f"Users org: {api_request_permissions_m2m['tenancy']['user'].id}")
                print(f"global org: {api_request_permissions_m2m['tenancy']['global'].id}")
                print(f'Failed returned row was: {row}')

        assert only_from_user_org
        try:
            the_model1.delete()
        except:
            pass
        try:
            the_model2.delete()
        except:
            pass
        try:
            the_model3.delete()
        except:
            pass



    def test_api_add_exception_m2m_model(self, mocker, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions_m2m, model_kwargs, kwargs_api_create, model
    ):
        """ API action capture exception

        Ensure that during a `Create` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions_m2m['user']['add'] )


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        # the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        # kwargs_create['model'] = the_model.model.id
        kwargs_create['created_by'] = api_request_permissions_m2m['user']['add'].id
        kwargs_create['organization'] = api_request_permissions_m2m['tenancy']['user'].id

        mocker.patch(
            f'{model.__module__}.{model.__name__}.objects.create',
            side_effect = param_exception("an integrity error occured....")
        )

        mocker.patch(
            "access.managers.tenancy.TenancyManager.create",
            side_effect = param_exception("an integrity error occured....")
        )


        try:

            response = client.post(
                path = url,
                data = kwargs_create,
                content_type = 'application/json'
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.post(
                    path = the_model.get_url( many = False ),
                    data = kwargs_create
                )

            except NoReverseMatch:

                pass


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content



    def test_api_change_exception_m2m_model(self, mocker, model, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions_m2m, model_kwargs
    ):
        """ API action capture exception

        Ensure that during a `Change` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions_m2m['user']['change'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        mocker.patch(
            f"{model.__module__}.{model.__name__}.save",
            side_effect = param_exception("an integrity error occured....")
        )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content



    def test_api_delete_exception_m2m_model(self, mocker, model, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions_m2m, model_kwargs
    ):
        """ API action capture exception

        Ensure that during a `Delete` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions_m2m['user']['delete'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        mocker.patch(
            f"{model.__module__}.{model.__name__}.delete",
            side_effect = param_exception("an integrity error occured....")
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content
