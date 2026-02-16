import datetime
from time import sleep
import pytest

from django.apps import apps
from django.db import models



class CenturionAuditEntryModelTestCases:
    """ Centurion Audit Entry Test Suite

    This test suite is intended to be included in ALL models functional test
    suites
    """


    @staticmethod
    def kwargs_to_audit_entry(model_kwargs, instance, audit_entry,
        is_create = True, is_edit = False
    ) -> dict:

        kwargs_converted = {}

        if is_create or is_edit:

            kwargs_converted.update({
                'id': instance.id,
                'created': instance.created.isoformat(timespec='seconds'),
                'modified': instance.modified.isoformat(timespec='seconds'),
            })


            if 'modified' not in kwargs_converted:

                kwargs_converted.update({
                    'modified': instance.modified.isoformat(timespec='seconds'),
                })


        for name, value in model_kwargs.items():

            if isinstance(value, models.Model):

                kwargs_converted.update({
                    f'{name}_id': value.id
                })

            elif isinstance(value, list):

                values = []

                for item in value:

                    if isinstance(item, models.Model):

                        values += [ item.id ]

                    else:

                        values += [ item ]

                kwargs_converted.update({
                    name: values
                })


            else:

                if isinstance(getattr(instance, name), datetime.datetime):

                    kwargs_converted.update({
                        name: datetime.datetime.fromisoformat(
                            model_kwargs[name]
                        ).isoformat(timespec='seconds')
                    })

                else:

                    kwargs_converted.update({
                        name: value
                    })


        for model_field in instance._meta.get_fields():
            name = model_field.name

            if(
                name in kwargs_converted
                or f'{name}_id' in kwargs_converted
                or not hasattr(model_field, 'default')
                or (
                    model_field.auto_created
                )
            ):
                continue


            if is_create and not is_edit:

                kwargs_converted.update({
                    name: model_field.default if getattr(
                        model_field, 'default', None
                            ) != models.fields.NOT_PROVIDED else None
                })

            elif is_edit:

                if isinstance(model_field, models.ManyToManyField):

                    objs = getattr(instance, name).all()

                    if len(objs) == 0:

                        kwargs_converted.update({
                            name: None
                        })

                    else:

                        vals = []
                        for val in objs:
                            vals += [ val.id ]


                        vals = sorted(vals)

                        kwargs_converted.update({
                            name: vals
                        })


                else:

                    value = getattr(instance, name)

                    if(
                        isinstance(value, models.Model)
                    ):

                        kwargs_converted.update({
                            f'{name}_id': value.id
                        })

                    else:

                        kwargs_converted.update({
                            name: value
                        })


        return kwargs_converted



    @pytest.fixture( scope = 'function')
    def audit_entry(self, django_db_blocker,
        mocker, model, model_kwargs,
        model_centurionuser, kwargs_centurionuser
    ):

        if not model._audit_enabled:
            pytest.xfail( reason = 'model does not have audit enabled.' )

        if model._meta.abstract:
            pytest.xfail( reason = 'model is abstract. Test is N/A.' )

        with django_db_blocker.unblock():

            user = model_centurionuser.objects.create( **kwargs_centurionuser() )

            mocker.patch.object(model, 'context', { 'logger': None, model._meta.model_name: user })

            orig_kwargs = model_kwargs()


            kwargs_many_to_many = {}

            kwargs = {}

            for key, value in orig_kwargs.items():

                field = model._meta.get_field(key)

                if isinstance(field, models.ManyToManyField):

                    kwargs_many_to_many.update({
                        key: value
                    })

                else:

                    kwargs.update({
                        key: value
                    })


            instance = model.objects.create( **kwargs )


            for key, value in kwargs_many_to_many.items():

                field = getattr(instance, key)

                for entry in value:

                    field.add(entry)



            audit_entry = apps.get_model(
                app_label = instance._meta.app_label,
                model_name = str(instance.get_history_model_name()).lower()
            ).objects.get(
                model = instance
            )

        yield {
            'entry': audit_entry,
            'instance': instance,
            'kwargs': orig_kwargs,
            'user': user,
        }

        with django_db_blocker.unblock():
            instance.delete()



    @pytest.mark.audit_models
    @pytest.mark.functional
    def test_centurionaudit_create_entry_before(self, audit_entry ):
        """Test Centurion Audit Entry

        When creating a model ensure that the before field is an empty dict
        """

        assert audit_entry['entry'].before == {}



    @pytest.mark.audit_models
    @pytest.mark.functional
    def test_centurionaudit_create_entry_after(self, audit_entry ):
        """Test Centurion Audit Entry

        When creating a model ensure that the after field is correct
        """

        kwargs_converted_after = self.kwargs_to_audit_entry(
            model_kwargs = audit_entry['kwargs'],
            instance = audit_entry['instance'],
            audit_entry = audit_entry['entry'],
        )


        assert audit_entry['entry'].after == kwargs_converted_after



    @pytest.mark.audit_models
    @pytest.mark.functional
    def test_centurionaudit_edit_entry_before(self, audit_entry,
        model, model_kwargs
    ):
        """Test Centurion Audit Entry

        When editing a model (non m2m field) ensure that the before field is
        correct.
        """

        audit_entry['entry'].delete()

        orig_kwargs = audit_entry['kwargs']
        orig_edit_kwargs = model_kwargs()

        kwargs_many_to_many = {}

        edit_model_kwargs = {}

        for key, value in orig_edit_kwargs.items():

            field = model._meta.get_field(key)

            if isinstance(field, models.ManyToManyField):

                kwargs_many_to_many.update({
                    key: value
                })

            else:

                edit_model_kwargs.update({
                    key: value
                })


        instance = audit_entry['instance']

        orig_kwargs.update({
            'modified': instance.modified.isoformat(timespec='seconds'),
        })

        for name, value in edit_model_kwargs.items():

            if(
                getattr(instance, name) == value
            ):
                continue


            setattr(instance, name, value)

            instance.save()

            audit_entry = apps.get_model(
                app_label = instance._meta.app_label,
                model_name = str(instance.get_history_model_name()).lower()
            ).objects.get(
                model = instance
            )

            kwargs_converted_after = self.kwargs_to_audit_entry(
                model_kwargs = orig_kwargs,
                instance = instance,
                audit_entry = audit_entry,
                is_edit = True,
            )

            assert audit_entry.before == kwargs_converted_after

            audit_entry.delete()

            orig_kwargs.update({
                name: value,
                'modified': instance.modified.isoformat(timespec='seconds'),
            })



    @pytest.mark.audit_models
    @pytest.mark.functional
    def test_centurionaudit_edit_entry_before_m2m_fields(self, audit_entry,
        model, model_kwargs
    ):
        """Test Centurion Audit Entry

        When editing a model (m2m field) ensure that the before field is
        correct.
        """

        audit_entry['entry'].delete()

        orig_kwargs = audit_entry['kwargs']
        orig_edit_kwargs = model_kwargs()

        kwargs_many_to_many = {}

        edit_model_kwargs = {}

        for key, value in orig_edit_kwargs.items():

            field = model._meta.get_field(key)

            if isinstance(field, models.ManyToManyField):

                kwargs_many_to_many.update({
                    key: value
                })

            else:

                edit_model_kwargs.update({
                    key: value
                })


        if len(kwargs_many_to_many) == 0:
            pytest.xfail( reason = 'Model does not contain any m2m fields' )


        instance = audit_entry['instance']

        orig_kwargs.update({
            'modified': instance.modified.isoformat(timespec='seconds'),
        })

        for name, value in kwargs_many_to_many.items():

            instance._before = instance.get_audit_values()

            if(
                getattr(instance, name) == value
            ):
                continue


            field = getattr(instance, name)

            for entry in value:

                field.add(entry)


            audit_entry = apps.get_model(
                app_label = instance._meta.app_label,
                model_name = str(instance.get_history_model_name()).lower()
            ).objects.get(
                model = instance
            )

            kwargs_converted_after = self.kwargs_to_audit_entry(
                model_kwargs = orig_kwargs,
                instance = instance,
                audit_entry = audit_entry,
                is_edit = True,
            )

            assert audit_entry.before == kwargs_converted_after

            audit_entry.delete()

            orig_kwargs.update({
                name: value,
                'modified': instance.modified.isoformat(timespec='seconds'),
            })



    @pytest.mark.audit_models
    @pytest.mark.functional
    def test_centurionaudit_edit_entry_after(self, audit_entry,
        model, model_kwargs
    ):
        """Test Centurion Audit Entry

        When editing a model (non m2m field) ensure that the after field is
        correct.
        """

        audit_entry['entry'].delete()

        orig_kwargs = audit_entry['kwargs']
        orig_edit_kwargs = model_kwargs()

        kwargs_many_to_many = {}

        edit_model_kwargs = {}

        for key, value in orig_edit_kwargs.items():

            field = model._meta.get_field(key)

            if isinstance(field, models.ManyToManyField):

                kwargs_many_to_many.update({
                    key: value
                })

            else:

                edit_model_kwargs.update({
                    key: value
                })


        instance = audit_entry['instance']

        orig_kwargs.update({
            'modified': instance.modified.isoformat(timespec='seconds'),
        })

        for name, value in edit_model_kwargs.items():

            if(
                getattr(instance, name) == value
            ):
                continue


            setattr(instance, name, value)

            instance.save()

            audit_entry = apps.get_model(
                app_label = instance._meta.app_label,
                model_name = str(instance.get_history_model_name()).lower()
            ).objects.get(
                model = instance
            )

            kwargs_converted_after = self.kwargs_to_audit_entry(
                model_kwargs = { name: value },
                instance = instance,
                audit_entry = audit_entry,
                is_edit = True,
            )

            assert audit_entry.after == { name: kwargs_converted_after[name] } if name in kwargs_converted_after else kwargs_converted_after[f'{name}_id']

            audit_entry.delete()



    @pytest.mark.audit_models
    @pytest.mark.functional
    def test_centurionaudit_edit_entry_after_m2m_fields(self, audit_entry,
        model, model_kwargs
    ):
        """Test Centurion Audit Entry

        When editing a model (m2m field) ensure that the after field is
        correct.
        """

        audit_entry['entry'].delete()

        orig_kwargs = audit_entry['kwargs']
        orig_edit_kwargs = model_kwargs()

        kwargs_many_to_many = {}

        for key, value in orig_edit_kwargs.items():

            field = model._meta.get_field(key)

            if isinstance(field, models.ManyToManyField):

                kwargs_many_to_many.update({
                    key: value
                })


        if len(kwargs_many_to_many) == 0:
            pytest.xfail( reason = 'Model does not contain any m2m fields' )


        instance = model.objects.get( id = audit_entry['instance'].id )

        instance._before = instance.get_audit_values()
        sleep(1)    # Must pause so that modified time is different.
        instance.save()

        orig_kwargs.update({
            'modified': instance.modified.isoformat(timespec='seconds'),
        })

        for name, value in kwargs_many_to_many.items():

            sleep(1)    # Must pause so that modified time is different.

            instance._before = instance.get_audit_values()

            if(
                getattr(instance, name) == value
            ):
                continue


            field = getattr(instance, name)

            for entry in value:

                field.add(entry)



            audit_entry = apps.get_model(
                app_label = instance._meta.app_label,
                model_name = str(instance.get_history_model_name()).lower()
            ).objects.get(
                model = instance
            )

            m2m_value = [ *orig_kwargs[name], *value ]
            orig_kwargs.update({
                name: m2m_value,
                'modified': instance.modified.isoformat(timespec='seconds'),
            })

            kwargs_converted_after = self.kwargs_to_audit_entry(
                model_kwargs = orig_kwargs,
                instance = instance,
                audit_entry = audit_entry,
                is_edit = True,
            )

            assert audit_entry.after == { name: kwargs_converted_after[name] }

            audit_entry.delete()
