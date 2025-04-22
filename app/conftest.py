import pytest

from django.test import (
    TestCase
)

from access.models.organization import Organization



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

        request.cls.item.delete()



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
