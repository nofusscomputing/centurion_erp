import datetime
import pytest
import os
import sqlite3
import sys

from django.core.management import call_command
from django.conf import settings
from django.test import (
    TestCase
)

from access.models.tenant import Tenant



@pytest.fixture(scope="session", autouse = True)
def load_sqlite_fixture(django_db_setup, django_db_blocker):
    """
    Load the SQLite database from an SQL dump file.
    This runs during test setup and loads the schema and data via SQLite directly.
    """
    db_path = settings.DATABASES['default']['NAME']
    sql_file_path = os.path.join('app/fixtures', 'fresh_db.sql')


    with django_db_blocker.unblock():
        with open(sql_file_path, 'r') as f:
            sql_script = f.read()
        conn = sqlite3.connect(db_path)
        try:
            conn.executescript(sql_script)
        finally:
            conn.close()

    
    with django_db_blocker.unblock():

        call_command('loaddata','fresh_db')



def pytest_report_header(config):

    print(f"Command-line arguments: {config.invocation_params.args}")
    print(f"Config file options: {config.getini('addopts')}")


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

    arg_values:list = None

    fixture_parameters: list = []

    parameterized_test = False

    parameterized_key: str = None

    if {'parameterized'} <= set(metafunc.fixturenames):

        for mark in metafunc.definition.own_markers:    # Skip tests markd to skip

            if mark.name == 'skip':
                return None

        for mark in getattr(metafunc.cls, 'pytestmark', []):    # Skip test suite markd to skip

            if mark.name == 'skip':
                return None

        all_fixture_parameters = metafunc.fixturenames

        fixture_parameters += ['parameterized']

        for i in range(0, len(metafunc.fixturenames)):

            if (
                str(all_fixture_parameters[i]).startswith('param_')
                and not str(all_fixture_parameters[i]).startswith('param_key_')
            ):

                fixture_parameters += [ all_fixture_parameters[i] ]


            elif str(all_fixture_parameters[i]).startswith('param_key_'):

                parameterized_key = str( all_fixture_parameters[i] ).replace('param_key_', '')

                if len(fixture_parameters) == 1:

                    fixture_parameters += [ all_fixture_parameters[i] ]

                else:

                    fixture_parameters[1] = all_fixture_parameters[i]


        parameterized_test = len(fixture_parameters) > 0


    if parameterized_test:

        values = {}


        cls = getattr(metafunc, "cls", None)

        if cls:

            for base in reversed(cls.__mro__):

                base_values = getattr(base, 'parameterized_' + parameterized_key, None)

                if isinstance(base_values, property):

                    base_values = getattr(base(), 'parameterized_' + parameterized_key, None)

                if not isinstance(base_values, dict):

                    continue

                if len(values) == 0 and len(base_values) > 0:

                    values.update(base_values)

                    continue

                for key, value in values.items():

                    if(
                        type(value) is not dict
                        or key not in base_values
                    ):

                        continue

                    if key not in values:

                        values.update({
                            key: base_values[key]
                        })

                    else:

                        values[key].update( base_values[key] )


                for key, value in base_values.items():

                    if key not in values:

                        values.update({
                            key: base_values[key]
                        })


        if values:

            ids = []

            arg_values:list = []

            for item in values.items():

                ids_name = item[0]

                item_values:tuple = ()

                length = len(item)

                is_key_value: bool = True

                if type(item[1]) is not dict:

                    continue


                item_values += ( None, None, item[0])

                for key in fixture_parameters:

                    if key in [ fixture_parameters[0], fixture_parameters[1], fixture_parameters[2], ]:
                        # these values are already defined in `item_values`
                        # fixture_parameters[0] = parameterized.
                        # fixture_parameters[1] = param_key
                        # fixture_parameters[2] = the dict name

                        continue

                    if(
                        str(key).startswith('param_')
                        and not str(key).startswith('param_key_')
                    ):

                        key = str(key).replace('param_', '')

                        if (
                            type(item[1]) is not dict
                            or item[1].get(key, 'key-does_not-exist') == 'key-does_not-exist'
                        ):

                            item_values = ()

                            continue


                        if key in item[1]:

                            item_values += ( item[1][key], )

                            if type(item[1][key]) is type:

                                ids_name += '_' + getattr(item[1][key], '__name__', 'err_generate_tests').lower()

                            elif callable(item[1][key]):

                                ids_name  += '_' + item[1][key].__name__

                            else:

                                ids_name += '_' + str(item[1][key]).lower()


                if(
                    len(item_values) > 0
                    and len(fixture_parameters) == len(item_values)
                ):

                    arg_values += [ item_values ]

                    ids += [ ids_name, ]


            if len(arg_values) > 0:

                metafunc.parametrize(
                    argnames = [
                        *fixture_parameters
                    ],
                    argvalues = arg_values,
                    ids = ids,
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
def create_model_random_data_five(request, django_db_blocker):
    """Create the specified model with random data

    **Note:** Dont use this fixture yet. More testing is required

    Yields:
        models.Model: Created Model
    """


    from django.db import models
    from django.core.files.base import ContentFile
    import random
    import os
    from faker import Faker

    from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel, OneToOneRel

    fake = Faker()

    _unique_counter = {}

    created_instances = {}

    def generate_unique_string(length=8):

        base = fake.word()

        counter = _unique_counter.get(base, 0) + 1

        _unique_counter[base] = counter

        return f"{base}_{counter}"[:length]


    def generate_random_file():

        return ContentFile(b"dummydata", name=f"{generate_unique_string(5)}.txt")

    def get_random_choice(choices):

        valid_choices = [choice[0] for choice in choices if not isinstance(choice[1], (list, tuple))]

        return random.choice(valid_choices or [None])


    def create_sample_instance(model_class, seen=None, except_fields = [], recurse_depth = 0):

        if seen is None:

            seen = set()


        recurse_depth += 1

        if recurse_depth == 3:

            return None


        if model_class in created_instances:

            return created_instances[model_class]


        if model_class in seen:

            return None


        seen.add(model_class)

        field_data = {}

        m2m_data = {}

        # Only iterate over concrete, editable fields
        for field in model_class._meta.get_fields():

            # if field.auto_created and not field.concrete:
            #     continue  # Skip reverse relations like ManyToOneRel

            if isinstance(field, (ManyToOneRel, ManyToManyRel, OneToOneRel)):

                continue  # Skip reverse relationships only


            if getattr(field, 'primary_key', False) or field.name in ['id', 'pk']:

                continue

            if field.name in except_fields:

                continue

            if isinstance(field, models.ManyToManyField):

                related_model = field.related_model

                related_instance = create_sample_instance(related_model, seen)

                if related_instance:

                    m2m_data[field.name] = [related_instance]


            elif hasattr(field, 'choices') and field.choices:

                field_data[field.name] = get_random_choice(field.choices)

            elif isinstance(field, models.CharField):

                field_data[field.name] = generate_unique_string(length=field.max_length or 12)

            elif isinstance(field, models.TextField):

                field_data[field.name] = generate_unique_string(length=200)

            elif isinstance(field, models.EmailField):

                field_data[field.name] = f"{generate_unique_string(8)}@example.com"

            elif isinstance(field, models.IntegerField):

                field_data[field.name] = random.randint(1, 99999)

            elif isinstance(field, models.FloatField):

                field_data[field.name] = random.uniform(1.0, 1000.0)

            elif isinstance(field, models.DecimalField):

                field_data[field.name] = round(random.uniform(1.0, 1000.0), field.decimal_places)

            elif isinstance(field, models.BooleanField):

                field_data[field.name] = random.choice([True, False])

            elif isinstance(field, models.DateField):

                field_data[field.name] = fake.date()

            elif isinstance(field, models.DateTimeField):

                field_data[field.name] = fake.date_time()

            elif isinstance(field, models.TimeField):

                field_data[field.name] = fake.time()

            elif isinstance(field, models.UUIDField):

                field_data[field.name] = fake.uuid4()

            elif isinstance(field, models.IPAddressField):

                field_data[field.name] = fake.ipv4()

            elif isinstance(field, models.GenericIPAddressField):

                field_data[field.name] = fake.ipv6()

            elif isinstance(field, models.SlugField):

                field_data[field.name] = fake.slug()

            elif isinstance(field, models.BinaryField):

                field_data[field.name] = os.urandom(10)

            elif isinstance(field, models.JSONField):

                field_data[field.name] = {generate_unique_string(4): random.randint(1, 10)}

            elif isinstance(field, (models.FileField, models.ImageField)):

                field_data[field.name] = generate_random_file()

            elif isinstance(field, (models.ForeignKey, models.OneToOneField)):

                related_model = field.related_model

                if model_class == related_model:

                    related_instance = create_sample_instance(related_model, seen=None, except_fields=except_fields, recurse_depth = recurse_depth)

                else:

                    related_instance = create_sample_instance(related_model, seen)


                if related_instance:

                    field_data[field.name] = related_instance


        with django_db_blocker.unblock():

            instance = model_class.objects.create(**field_data)

            created_instances[model_class] = instance

            for field_name, related_instances in m2m_data.items():

                getattr(instance, field_name).set(related_instances)


            seen.remove(model_class)


        return instance


    yield create_sample_instance


    with django_db_blocker.unblock():

        for model_class, model in created_instances.items():

            model.delete()



@pytest.fixture( scope = 'class')
def organization_one(django_db_blocker):

    item = None

    with django_db_blocker.unblock():

        random_str = datetime.datetime.now(tz=datetime.timezone.utc)

        item = Tenant.objects.create(
            name = 'org one from global' + str(random_str)
        )

    yield item

    with django_db_blocker.unblock():

        try:
            item.delete()
        except:
            pass



@pytest.fixture( scope = 'class')
def organization_two(django_db_blocker):

    item = None

    with django_db_blocker.unblock():

        random_str = datetime.datetime.now(tz=datetime.timezone.utc)

        item = Tenant.objects.create(
            name = 'org two from global' + str(random_str)
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


@pytest.fixture( scope = 'function')
def fake_view():


    class MockView:

        class MockRequest:

            class MockUser:

                id: int

                pk: int

            user = None

            def __init__(cls, user = 0):

                if user != 0:

                    cls.user = user

                # cls.user.id = user_id
                # cls.user.pk = user_id


        _has_import: bool
        """User Permission

        get_permission_required() sets this to `True` when user has import permission.
        """

        _has_purge: bool
        """User Permission

        get_permission_required() sets this to `True` when user has purge permission.
        """

        _has_triage: bool
        """User Permission

        get_permission_required() sets this to `True` when user has triage permission.
        """

        action:str
        """ The View Action

        This must be set to whatever is occuring
        """

        request: MockRequest

        def __init__(cls,
            _has_import: bool = False,
            _has_purge: bool = False,
            _has_triage: bool = False,
            action: str = 'create',
            user = 0,
        ):

            cls.request = cls.MockRequest(
                user = user
            )

            cls._has_import = _has_import
            cls._has_purge = _has_purge
            cls._has_triage = _has_triage
            cls.action = action


    fake_view = MockView

    yield fake_view

    del fake_view
