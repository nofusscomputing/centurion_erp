from django.db import migrations



def postgres_index_fix(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return

    sql_statements = [
        # DeviceModel.manufacturer index fix
        """
        DO $$
        DECLARE
            idx TEXT;
        BEGIN
            SELECT indexname INTO idx
            FROM pg_indexes
            WHERE tablename='itam_devicemodel'
              AND indexname LIKE 'itam_devicemodel_manufacturer_id_%'
            LIMIT 1;

            IF idx IS NOT NULL THEN
                EXECUTE format(
                    'ALTER INDEX %I RENAME TO %I',
                    idx,
                    replace(idx, 'manufacturer_id', 'manufacturer_old_id')
                );
            END IF;
        END
        $$;
        """,

        # OperatingSystem.publisher index fix
        """
        DO $$
        DECLARE
            idx TEXT;
        BEGIN
            SELECT indexname INTO idx
            FROM pg_indexes
            WHERE tablename='itam_operatingsystem'
              AND indexname LIKE 'itam_operatingsystem_publisher_id_%'
            LIMIT 1;

            IF idx IS NOT NULL THEN
                EXECUTE format(
                    'ALTER INDEX %I RENAME TO %I',
                    idx,
                    replace(idx, 'publisher_id', 'publisher_old_id')
                );
            END IF;
        END
        $$;
        """,

        # Software.publisher index fix
        """
        DO $$
        DECLARE
            idx TEXT;
        BEGIN
            SELECT indexname INTO idx
            FROM pg_indexes
            WHERE tablename='itam_software'
              AND indexname LIKE 'itam_software_publisher_id_%'
            LIMIT 1;

            IF idx IS NOT NULL THEN
                EXECUTE format(
                    'ALTER INDEX %I RENAME TO %I',
                    idx,
                    replace(idx, 'publisher_id', 'publisher_old_id')
                );
            END IF;
        END
        $$;
        """,
    ]

    with schema_editor.connection.cursor() as cursor:

        for sql in sql_statements:

            cursor.execute(sql)



class Migration(migrations.Migration):

    dependencies = [
        ('itam', '0016_alter_software_organization'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devicemodel',
            old_name='manufacturer',
            new_name='manufacturer_old',
        ),
        migrations.RenameField(
            model_name='operatingsystem',
            old_name='publisher',
            new_name='publisher_old',
        ),
        migrations.RenameField(
            model_name='software',
            old_name='publisher',
            new_name='publisher_old',
        ),
        migrations.RunPython(postgres_index_fix, migrations.RunPython.noop),
    ]
