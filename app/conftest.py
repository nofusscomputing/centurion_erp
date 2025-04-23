import pytest
import sys

from django.test import (
    TestCase
)

from access.models.organization import Organization



def pytest_configure(config):

    print("\n--- Pytest Launch Arguments ---")
    print(f"Command-line arguments: {config.invocation_params.args}")
    print(f"Config file options: {config.getini('addopts')}")
    print("\n-------------------------------")


def pytest_pycollect_makeitem(collector, name, obj):
    """PyTest Test Creation

    Create PyTest Test Classes if the classname ends in `Test`
    and is not inheriting from django,test.TestCase.
    """

    if (
        isinstance(obj, type)
        and name.endswith("PyTest")
        and not issubclass(obj, TestCase)    # Don't pickup any django unittest.TestCase
    ):
        return pytest.Class.from_parent(parent=collector, name=name)



@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):    # pylint: disable=W0613:unused-argument
    pass



def pytest_generate_tests(metafunc):

    # test_no_value = {"test_name", "test_value", "expected"} <= set(metafunc.fixturenames)

    # test_value = {"test_name", "test_value", "return_value", "expected"} <= set(metafunc.fixturenames)

    if {"test_name", "test_value", "expected"} <= set(metafunc.fixturenames):
        values = {}


        cls = getattr(metafunc, "cls", None)

        if cls:

            for base in reversed(cls.__mro__):

                base_values = getattr(base, "parametrized_test_data", [])

                if isinstance(base_values, dict):

                    values.update(base_values)


        if values:

            metafunc.parametrize(
                argnames = (
                    "test_name", "test_value", "expected"
                ),
                argvalues = [
                    (field, field, expected) for field, expected in values.items()
                ],
                ids = [
                    str( field.replace('.', '_') + '_' + getattr(expected, '__name__', 'None').lower() ) for field, expected in values.items()
                ],
            )



@pytest.fixture( scope = 'class')
def create_model(request, django_db_blocker):

    item = None

    with django_db_blocker.unblock():

        item = request.cls.model.objects.create(
            **request.cls.kwargs_create_item
        )

        request.cls.item = item

    yield item

    with django_db_blocker.unblock():

        item.delete()



@pytest.fixture( scope = 'class')
def organization_one(django_db_blocker):

    item = None

    with django_db_blocker.unblock():

        item = Organization.objects.create(
            name = 'org one'
        )

    yield item

    with django_db_blocker.unblock():

        item.delete()



@pytest.fixture( scope = 'class')
def organization_two(django_db_blocker):

    item = None

    with django_db_blocker.unblock():

        item = Organization.objects.create(
            name = 'org two'
        )

    yield item

    with django_db_blocker.unblock():

        item.delete()



@pytest.fixture
def recursearray() -> dict[dict, str, any]:
    """Recursive dict lookup

    Search through a dot notation of dict paths and return the data assosiated
    with that dict.

    Args:
        obj (dict): dict to use for the recusive lookup
        key (str): the dict keys in dot notation. i.e. dict_1.dict_2
        rtn_dict (bool, optional): return the dictionary and not the value.
            Defaults to False.

    Returns:
        dict[dict, str, any]: lowest dict found. dict values are obj, key and value.

    """

    def _recursearray(obj: dict, key:str) -> dict[dict, str, any]:

        item = None

        if key in obj:
            
            return {
                'obj': obj,
                'key': key,
                'value': obj[key]
            }

        keys = []

        if '.' in key:

            keys = key.split('.')


            for k, v in obj.items():

                if k == keys[0] and isinstance(v,dict):

                    if keys[1] in v:

                        item = _recursearray(v, key.replace(keys[0]+'.', ''))

                        return {
                            'obj': item['obj'],
                            'key': item['key'],
                            'value': item['value']
                        }

                elif k == keys[0] and isinstance(v,list):

                    try:

                        list_key = int(keys[1])

                        try:

                            item = v[list_key]

                            v = item


                            if keys[2] in v:

                                item = _recursearray(v, key.replace(keys[0]+'.'+keys[1]+'.', ''))

                                return {
                                    'obj': item['obj'],
                                    'key': item['key'],
                                    'value': item['value']
                                }

                        except IndexError:

                            print( f'Index {keys[1]} does not exist. List had a length of {len(v)}', file = sys.stderr )

                            return None

                    except ValueError:

                        print( f'{keys[1]} does not appear to be a number.', file = sys.stderr )

                        return None

        return {
            'obj': obj,
            'key': key,
            'value': None
        }

    return _recursearray
