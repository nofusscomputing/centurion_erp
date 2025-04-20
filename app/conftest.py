import pytest

from django.test import (
    TestCase
)



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
