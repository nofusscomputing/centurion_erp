import pytest
import re

from django.core.exceptions import ValidationError

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_model import (
    ITAMAssetBaseModelInheritedCases
)



@pytest.mark.model_itassetmodel
class ITAssetModelModelTestCases(
    ITAMAssetBaseModelInheritedCases
):



        itassetmodel_regex_params = [
                ('wlp3s', 'wlp3s', None, None),
                ('wlp3s0', 'wlp3s', '0', None),
                ('wlp3s44', 'wlp3s', '44', None),
                ('wlp344s0', 'wlp344s', '0', None),
                ('wlp344s544', 'wlp344s', '544', None),
                ('LAN0', 'LAN', '0', None),
                ('LAN-0', 'LAN-', '0', None),
                ('LAN0-5', 'LAN', '0', '5'),
                ('LAN11-22', 'LAN', '11', '22'),

            ]



        @pytest.mark.parametrize(
            argnames = [ 'value', 'name', 'lowest', 'highest' ],
            argvalues = itassetmodel_regex_params,
            ids = [val[0] for val in itassetmodel_regex_params]
        )
        def test_function_create_asset_connections_name_templating_name(self,
            model, 
            value, name, lowest, highest
        ):
            """Test class function
            
            Confirm that different formats of the connections name are detected
            properly.
            """
            
            regex = model._regex_template_connect_name


            multi_name = re.match(
                regex,
                value
            )

            assert name == multi_name.group( 'name' )



        @pytest.mark.parametrize(
            argnames = [ 'value', 'name', 'lowest', 'highest' ],
            argvalues = itassetmodel_regex_params,
            ids = [val[0] for val in itassetmodel_regex_params]
        )
        def test_function_create_asset_connections_name_templating_lowest(self,
            model, 
            value, name, lowest, highest
        ):
            """Test class function
            
            Confirm that different formats of the connections lowest value is detected
            properly.
            """
            
            regex = model._regex_template_connect_name


            multi_name = re.match(
                regex,
                value
            )

            assert lowest == multi_name.group( 'lowest' )



        @pytest.mark.parametrize(
            argnames = [ 'value', 'name', 'lowest', 'highest' ],
            argvalues = itassetmodel_regex_params,
            ids = [val[0] for val in itassetmodel_regex_params]
        )
        def test_function_create_asset_connections_name_templating_highest(self,
            model, 
            value, name, lowest, highest
        ):
            """Test class function
            
            Confirm that different formats of the connections highest value is detected
            properly. i.e.
            """
            
            regex = model._regex_template_connect_name


            multi_name = re.match(
                regex,
                value
            )

            assert highest == multi_name.group( 'highest')



        def test_function_create_asset_connections_creates_connections(self,
            model, model_kwargs, model_itassetrelationships, kwargs_itassetrelationships,
            model_itasset, kwargs_itasset
        ):
            """Test class function
            
            When this function is called an `it_asset` is passed to it. Then using the
            connections on `self`, they are created and connected to the passed `it_asset`.
            """

            kwargs = kwargs_itassetrelationships()
            kwargs['name'] = 'LAN0-1'

            template_model = kwargs['parent_asset_model']
            connection = model_itassetrelationships.objects.create( **kwargs )

            template_connection = model_itassetrelationships.objects.filter(
                parent = None,
                parent_asset_model = template_model
            )

            assert len(template_connection) == 1, \
                'Template connection must exist for test to function'

            kwargs = kwargs_itasset()
            kwargs['device_model'] = template_model

            asset = model_itasset.objects.create( **kwargs )

            connections_created = model_itassetrelationships.objects.filter(
                parent = asset
            )

            assert len(connections_created) == 2




class ITAssetModelModelInheritedCases(
    ITAssetModelModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelModelPyTest(
    ITAssetModelModelTestCases,
):
    pass
