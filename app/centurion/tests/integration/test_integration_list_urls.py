import re

import pytest

from django.urls import get_resolver

from centurion.tests.integration.test_integration_common import IntegrationCommon



@pytest.mark.integration
@pytest.mark.regression
class URLChecksPyTest(
    IntegrationCommon
):


    list_view_urls = IntegrationCommon.list_urls(urlpatterns = get_resolver().url_patterns)


    @pytest.mark.parametrize(
        argnames = "url_path",
        argvalues = [
            url for url in list_view_urls if( url in IntegrationCommon.NO_AUTH_URLS )
        ],
        ids = [
            re.sub(r'[^\w_\-.:]', '_', url) for url in list_view_urls if( url in IntegrationCommon.NO_AUTH_URLS )
        ],
    )
    def test_urls_no_auth_required(self, url_path, auto_login_client):
        url = f"{IntegrationCommon.API_URL}/{url_path}"

        response = auto_login_client.request("GET", url)

        if response.status_code == 502:    # cater for complete Gunicorn restart
            time.sleep(10)
            response = auto_login_client.request("GET", url)

        assert response.status_code == 200



    @pytest.mark.permissions
    @pytest.mark.parametrize(
        argnames = "url_path",
        argvalues = [
            url for url in list_view_urls if(
                url not in IntegrationCommon.NO_AUTH_URLS
                and url not in IntegrationCommon.URLS_LIST_VIEW_AUTH_REQUIRED_EXCLUDED
                )
        ],
        ids = [
            re.sub(r'[^\w_\-.:]', '_', url) for url in list_view_urls if(
                url not in IntegrationCommon.NO_AUTH_URLS
                and url not in IntegrationCommon.URLS_LIST_VIEW_AUTH_REQUIRED_EXCLUDED
            )
        ],
    )
    def test_urls_list_view_auth_required(self, url_path, auto_login_client):
        url = f"{IntegrationCommon.API_URL}/{url_path}"

        response = auto_login_client.request("GET", url)

        if response.status_code == 502:    # cater for complete Gunicorn restart
            time.sleep(10)
            response = auto_login_client.request("GET", url)

        assert response.status_code == 401



    @pytest.mark.permissions
    @pytest.mark.parametrize(
        argnames = "url_path",
        argvalues = [
            url for url in list_view_urls if( 
                url not in IntegrationCommon.NO_AUTH_URLS
                and url not in IntegrationCommon.URLS_LIST_VIEW_AUTH_REQUIRED_AUTHENTICATED_EXCLUDED
            )
        ],
        ids = [
            re.sub(r'[^\w_\-.:]', '_', url) for url in list_view_urls if(
                url not in IntegrationCommon.NO_AUTH_URLS
                and url not in IntegrationCommon.URLS_LIST_VIEW_AUTH_REQUIRED_AUTHENTICATED_EXCLUDED
                )
        ],
    )
    def test_urls_list_view_auth_required_authenticated(self, url_path, auto_login_client):
        url = f"{IntegrationCommon.API_URL}/{url_path}"

        response = auto_login_client.request(method = "GET", url = url, auth = True)

        if response.status_code == 502:    # cater for complete Gunicorn restart
            time.sleep(10)
            response = auto_login_client.request("GET", url)

        assert response.status_code == 200, response


    def test_urls_metrics(self, auto_login_client):
        """ Test Endpoint Metrics

        Ensure that the page returns HTTP/200
        """
        url = f"{IntegrationCommon.API_URL[0:-5]}:8080/metrics"

        response = auto_login_client.request(method = "GET", url = url, auth = False)

        assert response.status_code == 200, response
