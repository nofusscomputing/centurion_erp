---
title: Testing
description: Testing, Development documentation for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Unit and functional tests are written to aid in application stability and to assist in preventing regression bugs. As part of development the developer working on a Merge/Pull request is to ensure that tests are written. Failing to do so will more likely than not ensure that your Merge/Pull request is not merged.

We use PyTest as the testing framework. As such, All available features of pytest are available. We have slightly deviated from the standard naming convention wherein test class must be suffixed with `PyTest`. Please [see below](#writing-tests) for more details.


## Directory Structure

Each module is to contain a tests directory of the model being tested with a single file for grouping of what is being tested. for items that depend upon a parent model, the test file is to be within the child-models test directory named with format `test_<type>_<model name>_<component name>`. Format for the test filename is as follows:

- `Type` - The test type, which is one of `unit`, `functional`, `ui` etc.

- `model_name` -  the value of the models `verbose_name` with the space char `\s` replaced with underscore `_`.

- `component name` -  The component being tested, which is one of `ViewSet`, `Serializer`, `API` etc.

example file system structure showing the layout of the tests directory for a module.

``` text
.
├── tests
│   ├── functional
│   │   ├── __init__.py
│   │   └── <model name>
│           ├── test_functional_<model name>_api_fields.py
│           ├── test_functional_<model name>_api_permission.py
│           ├── test_functional_<model name>_api_metadata.py
│           ├── test_functional_<model name>_model.py
│   │       └── test_functional_<model name>_serializer.py
│   ├── __init__.py
│   ├── integration
│   │   ├── __init__.py
│   │   └── <model name>
│   │       └── test_<type>_<model name>_<component name>.py
│   ├── ui
│   │   ├── __init__.py
│   │   └── <model name>
│   │       └── test_<type>_<model name>_<component name>.py
│   └── unit
│       ├── __init__.py
│       └── <model name>
│           ├── test_unit_<model name>_model.py
│           ├── test_unit_<model name>_serializer.py
│           └── test_unit_<model name>_viewset.py

```

Tests are broken up into the type the test is (sub-directory to test), and they are `unit`, `functional`, `UI` and `integration`. These sub-directories each contain a sub-directory for each model they are testing.


## Writing Tests

We use class based tests with each test case being its own function. Naming of test classes is in `CamelCase` in format `<class name><suffix>`. `class name` is the name of the actual class being tested with the `suffix` being one of the following:

- `TestCases` - Contains the test cases for the class being tested.

    This class contains all of the tests for the area being tested.

- `InheritedCases` - Is to inherit from `TestCases` and contains any additional tests for classes that inherit from the class being tested

    This class is used by sub-models and/or sub-classes that inherit from the area being tested

- `PyTest` - **Not** to inherit from `TestCases`. This _special_ suffix tells pytest during test collection, to build the test suite using PyTest.

    This class is the class that test the actual object(s) being tested.

Do not deviate from the test class name suffix as we have setup pytest to automagically create the test classes based off of these names. For instance, classes that are suffixed (not prefixed as is the pytest norm), will be added as a test class and not as an abstract class.

Test Cases are to test one object and one object **only**. If the object to be tested contains multiple objects/moving parts, instantiate that object within a fixture. Some test may require that the test be setup before the tests begin. This is done via fixture called `class_setup` that is called with `scope='class', autouse = True`. Each test case must be documented using docstring.

!!! tip
    If you inherit from an `InheritedCases` Class and there is a `class_setup` fixture, don't forget to import this into your test suite. This ensures it's available for use when running tests

!!! tip
    If you find that a base classes variables are being mutated by other test classes, setup the variable within the base class as a property that contains the defaults as a variable within the function and returns the data as if the property was defined as a variable
    <!-- markdownlint-disable -->

    Don't do this as `my_variable` will be mutated by other test classes that inherit the base class.

    ``` py

    class MyTestClassBase:
    
        my_variable = 'a'



    class MyTestClass(
        MyTestClassBase
    ):
    
        my_variable = 'b'

    ```

    Instead, do this. now `MyTestClass` wont override variable `my_variable` which means when another test class inherits from `MyTestClassBase`, variable `my_variable` will always return the desired default value.

    ``` py

    class MyTestClassBase:

        @property
        def my_variable(self):
    
            default = 'a'
    
            return default.copy()



    class MyTestClass(
        MyTestClassBase
    ):

        my_variable = 'b'

    ```

    <!-- markdownlint-restore -->


### Fixtures

Fixtures are used to setup the test and to pass objects to test should they require it. We have some common and globally available fixtures, they are:

- `create_model` Creates the model from class var `kwargs_create_item: dict`

- `organization_one` Organization called `org one`

- `organization_two` Organization called `org two`

- `recursearray` Search through an array using dot notation (`dict.list.dict` i.e. `dict_1.2.dict_3`). The array can be a `dict`, `list` or combination of both.

!!! info
    Unless otherwise mentioned, fixtures are `scope = 'class'`

There may also be a requirement that you add additional fixtures, they are:

- Global Model Fixtures

    Locatation for the global fixtures is `app/tests/fixtures/`. Each model is to have a global fixture file added with name `model_<model name>` within this file the following fixtures are to be created:

    ``` py title="tests/fixtures/model_centurionmodel.py"
    import pytest

    from core.models.centurion import CenturionModel



    @pytest.fixture( scope = 'class')
    def model_centurionmodel():

        yield CenturionModel


    @pytest.fixture( scope = 'class')
    def kwargs_centurionmodel(kwargs_tenancyabstract):

        kwargs = {
            **kwargs_tenancyabstract,
            'model_notes': 'model notes txt',
            'created': '2025-05-23T00:00',
        }

        yield kwargs.copy()

    ```

    - `model` is to return the model class un-instantiated

    - `kwargs` the Kwargs required to create the model.

- `model` and `model_kwargs` These fixtures should be defined in `conftest.py` in the test suite files directory. _Only required if the model is required to be worked with._

    ``` py title="conftest.py"

    import pytest

    from itim.models.request_ticket import RequestTicket



    @pytest.fixture( scope = 'class')
    def model(request):

        yield RequestTicket

    
    @pytest.fixture( scope = 'class')
    def model_kwargs(request, kwargs_<model_name>):

        request.cls.kwargs_create_item = kwargs_<model_name>.copy()

        yield kwargs_<model_name>.copy()

        del request.cls.kwargs_create_item


    ```

Due to how pytest and pytest-django works, there is no method available for class based tests that allows both database access and inheritance. As such, all test classes are expected to have a fixture called `class_setup` that is `scope = 'class'` and `autouse = True` that is intended to serve as the method of setting up the test suite. This fixture should also include as dependencies any other fixture required for setup and in the order required for setup to finish without error. This fixture (`class_setup`) is also intended to be an over-writable fixture in parent classes should you need to customise the load order of fixtures.

!!! tip
    Fixtures that are `scope = 'class'` are unable to accept fixture `db` including other database related marks, which is problematic for a class fixture that requires database access. As a workaround the following works:
    <!-- markdownlint-disable -->

    ``` py
    @pytest.fixture( scope = 'class')
    def setup_post(self, django_db_blocker):
    
        with django_db_blocker.unblock():
    
            # db transactions
    
        yield item    # required so that cleanup can be done
                      # Note: use return if the db transaction was to create
                      # a single object.
    
        with django_db_blocker.unblock():
    
            # db transactions for cleanup

    ```

    <!-- markdownlint-restore -->


### API Permissions Tests

API Permissions tests are automagically created when `pytest collect` runs. Normally there will be nothing that needs to be done for this test suite. However if you find there is a requirement for adding additional API Permission Test Cases add an additional tests file. This file must be placed in path `<app name>/tests/functional/additional_<model name>_permissions_api.py`. The contents of this file is as follows:

``` py



class AdditionalTestCases:    # You must use this class name

    def test_my_test_case(self, fixture_name):

        # your test case logic.


```

Once this file is detected during `collect` the test cases in class `AdditionalTestCases`, will be included in the API Permission Test Suit for the model in question.


## Parameterizing Tests

To be able to paramertize any test case, the test must be setup to use PyTest. Within the test class the test data is required to be stored in a dictionary prefixed with string `paramaterized_<data_name>`. Variable `<data_name>` is the data key that you will specify within the test method.

Our test setup allows for class inheritance which means you can within each class of the inheritance chain, add the `paramaterized_<data_name>` attribute. If you do this, starting from the lowest base class, each class that specifies the `paramaterized_<data_name>` attribute will be merged. The merge is an overwrite of the classes previous base class, meaning that the classes higher in the chain will overwrite the value of the lower class in the inheritance chain. You can not however remove a key from attribute `paramaterized_<data_name>`.

The test method must be called with parameters:

- 'parameterized'

    Tells the test setup that this test case is a parameterized test.

- `param_key_<data_name>`

    Tells the test setup the suffix to use to find the test data. The value of variable `data_name` can be any value you wish as long as it only contains chars `a-z` and/or `_` (underscore). This value is also used in class parameter `paramaterized_<data_name>`.

- `param_<name>`

    Tells the test setup that this is data to be passed from the test. When test setup is run, these attributes will contain the test data. It's of paramount importance, that the dict You can have as many of these attributes you wish, as long as `<name>` is unique and `<name>` is always prefixed with `param_`. If you specify more than to parameters with the `param_` prefix, the value after the `param_` prefix, must match the dictionary key for the data you wish to be assigned to that parameter. what ever name you give the first `param_` key, will always receive the key name from the `parameterized_test_data` attribute in the test class.

    The value of `<name>` for each and in the order specified is suffixed to the test case name

``` py

class MyTestClassTestCases:


    parameterized_test_data: dict = {
        'key_1': {
            'expected': 'key_1'
        },
        'key_2': {
            'random': 'key_2'
        },
    }


class MyTestClassPyTest(
    MyTestClassTestCases
):

    parameterized_test_data: dict = {
        'key_2': {
            'random': 'value'
        }
        'key_3': {
            'expected': 'key_3',
            'is_type': bool
        }
    }


    parameterized_second_dict: dict = {
        'key_1': {
            'expected': 'key_1'
        },
    }

    def test_my_test_case_one(self, parameterized, param_key_test_data, param_value, param_expected):

        assert param_value == param_expected


    def test_my_test_case_two(self, parameterized, param_key_test_data, param_value, param_random):

        assert param_value == param_random


    def test_my_test_case_three(self, parameterized, param_key_test_data, param_value, param_is_type):

        my_test_dict = self.adict

        assert type(my_test_dict[param_value]) is param_is_type


    def test_my_test_case_four(self, parameterized, param_key_second_dict, param_arbitrary_name, param_expected):

        my_test_dict = self.a_dict_that_is_defined_in_the_test_class

        assert my_test_dict[param_arbitrary_name] == param_expected

```

In this example:

- The test class in this case is `MyTestClassPyTest` which inherits from `MyTestClassTestCases`. there are two parameterized variables: `test_data` and `second_dict`. Although, the concrete class attribute `parameterized_test_data` overrides the base classes variable of the same name, the test setup logic does merge `MyTestClassPyTest.parameterized_test_data` with `MyTestClassTestCases.parameterized_test_data`. So in this case the value dictionary `MyTestClassPyTest.parameterized_test_data[key_2][random]`, `value` will overwrite dictionary of the same name in the base class. In the same token, as dictionary `MyTestClassTestCases.parameterized_test_data[key_3]` does not exist, it will be added to the dictionary during merge so it exists in `MyTestClassPyTest.parameterized_test_data`

- test suite `MyTestClassPyTest` will create a total of five parmeterized test cases for the following reasons:

    - `test_my_test_case_one` will create two parameterized test cases.

        - will use data in attribute `test_data` prefixed with `parameterized_` as this is the attribute prefixed with `param_key_`.

        - `MyTestClassPyTest.parameterized_test_data['key_1']` is a dictionary, which contains key `expected` which is also one of the attributes specified with prefix `param_`

        - `MyTestClassPyTest.parameterized_test_data['key_3']` is a dictionary, which contains key `expected` which is also one of the attributes specified with prefix `param_`

    - `test_my_test_case_two` will create one parameterized test case.

        - will use data in attribute `test_data` prefixed with `parameterized_` as this is the attribute prefixed with `param_key_`.

        - `MyTestClassPyTest.parameterized_test_data['key_2']` is a dictionary, which contains key `random` which is also one of the attributes specified with prefix `param_`

    - `test_my_test_case_three` will create one parameterized test case.

        - will use data in attribute `test_data` prefixed with `parameterized_` as this is the attribute prefixed with `param_key_`.

        - `MyTestClassPyTest.parameterized_test_data['key_3']` is a dictionary, which contains key `is_type` which is also one of the attributes specified with prefix `param_`

    - `test_my_test_case_four` will create one parameterized test case.

        - will use data in attribute `second_dict` prefixed with `parameterized_` as this is the attribute prefixed with `param_key_`.

        - `MyTestClassPyTest.parameterized_second_dict['key_1']` is a dictionary, which contains key `expected` which is also one of the attributes specified with prefix `param_`


## Running Tests

Test can be run by running the following:

1. `pip install -r requirements_test.txt -r requirements.txt`

1. `make prepare`

1. `make test-unit` for running Unit tests or `make test-functional` for running Functional tests.

If your developing using VSCode/VSCodium the testing is available as is the ability to attach a debugger to the test.


## Test Case docs to be re-written

!!! note
    The documentation below this section are being re-factored to meet an updated method of testing (documentation above this section). Until **all** test suites/cases have been re-written, the docs within and below this section may still be applicable.

~~Unit and functional tests are written to aid in application stability and to assist in preventing regression bugs. As part of development the developer working on a Merge/Pull request is to ensure that tests are written. Failing to do so will more likely than not ensure that your Merge/Pull request is not merged.~~

User Interface (UI) test are written _if applicable_ to test the user interface to ensure that it functions as it should. Changes to the UI will need to be tested.

~~!!! note~~
    ~~As of release v1.3, the UI has moved to it's [own project](https://github.com/nofusscomputing/centurion_erp_ui) with the current Django UI feature locked and depreciated.~~

Integration tests **will** be required if the development introduces code that interacts with an independent third-party application.


### Available Test classes

To aid in development we have written test classes that you can inherit from for your test classes

- API Permission Checks

    _These test cases ensure that only a user with the correct permissions can perform an action against a Model within Centurion_

    - `api.tests.abstract.api_permissions_viewset.APIPermissionAdd` _Add permission checks_

    - `api.tests.abstract.api_permissions_viewset.APIPermissionChange` _Change permission check_

    - `api.tests.abstract.api_permissions_viewset.APIPermissionDelete` _Delete permission check_

    - `api.tests.abstract.api_permissions_viewset.APIPermissionView` _View permission check_

    - `api.tests.abstract.api_permissions_viewset.APIPermissions` _Add, Change, Delete and View permission checks_

- API Field Checks

    _These test cases ensure that all of the specified fields are rendered as part of an API response_

    - `api.tests.abstract.api_fields.APICommonFields` _Fields that should be part of ALL API responses_

    - `api.tests.abstract.api_fields.APIModelFields` _Fields that should be part of ALL model API Responses. Includes `APICommonFields` test cases_

    - `api.tests.abstract.api_fields.APITenancyObject` _Fields that should be part of ALL Tenancy Object model API Responses. Includes `APICommonFields` and `APIModelFields` test cases_


### Writing Tests - Old

~~We use class based tests. Each class will require a `setUpTestData` method for test setup. To furhter assist in the writing of tests, we have written the test cases for common items as an abstract class. You are advised to inherit from our test classes _(see above)_ as a starting point and extend from there.~~

~~Naming of test classes is in `CamelCase` in format `<Model Name><what's being tested>` for example the class name for device model history entry tests would be `DeviceHistory`.~~

~~Test setup is written in a method called `setUpTestData` and is to contain the setup for all tests within the test class.~~

~~Test cases themselves are written within the test class within an appropriately and uniquely named method. Each test case is to test **one** and only one item.~~

Example of a model history test class.

``` py

import pytest
import requests

from django.test import TestCase, Client

from core.models.history import History
from core.tests.abstract.history_entry import HistoryEntry
from core.tests.abstract.history_entry_parent_model import HistoryEntryParentItem



class DeviceHistory(TestCase, HistoryEntry, HistoryEntryParentItem):


    model = Device


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

```

~~Each module is to contain a tests directory of the model being tested with a single file for grouping of what is being tested. for items that depend upon a parent model, the test file is to be within the child-models test directory named with format `test_<model>_<parent app>_<parent model name>`~~

~~example file system structure showing the layout of the tests directory for a module.~~

``` text
.
├── tests
│   ├── functional
│   │   ├── __init__.py
│   │   └── <model name>
│   │       └── test_<model name>_a_tast_name.py
│   ├── __init__.py
│   ├── integration
│   │   ├── __init__.py
│   │   └── <model name>
│   │       └── test_<model name>_a_tast_name.py
│   ├── ui
│   │   ├── __init__.py
│   │   └── <model name>
│   │       └── test_<model name>_a_tast_name.py
│   └── unit
│       ├── __init__.py
│       └── <model name>
│           ├── test_<model name>.py
│           ├── test_<model name>_api.py
│           ├── test_<model name>_core_history.py
│           ├── test_<model name>_history_permission.py
│           ├── test_<model name>_permission_api.py
│           ├── test_<model name>_permission.py
│           ├── test_<model name>_serializer.py
│           └── test_<model name>_viewsets.py

```

~~Tests are broken up into the type the test is (sub-directory to test), and they are `unit`, `functional`, `UI` and `integration`. These sub-directories each contain a sub-directory for each model they are testing.~~

Items to test include, and are not limited to:

- CRUD permissions admin site

- CRUD permissions api site

- can only access organization object

- can access global object (still to require model CRUD permission)

- history

    - saves history with parent pk and parent class

        add to model class the following

        ``` py

        @property
        def parent_object(self):
            """ Fetch the parent object """
            
            return self.<item that is the parent>

        ```

        history should now be auto saved as long as class `core.mixin.history_save.SaveHistory` is inherited by model.

    - history is deleted when item deleted if `parent_pk=None` or if has `parent_pk` deletes history on parent pk being deleted.

- model - _any customizations_

- API Fields

    _Field(s) exists, Type is checked_

- Serializer Validations
