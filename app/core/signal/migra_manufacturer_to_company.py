from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import ContentType
from django.db.models.signals import (
    post_migrate,
)
from django.dispatch import receiver

from centurion.logging import CenturionLogger



def migrate_itam_devicemodel_manufacturer(manufacturer, company, log, user):

    DeviceModel = apps.get_model(
        app_label = 'itam',
        model_name = 'devicemodel'
    )

    for device_model in DeviceModel.objects.filter( manufacturer_old = manufacturer ):

        try:

            type(device_model).context.update({
                'logger': log,
                device_model._meta.model_name: user
            })
            device_model.manufacturer = company
            device_model.save()

            device_model.manufacturer_old = None
            device_model.save()

            log.info(
                msg = f'Migrated Device Model {device_model} to use company {company}'
            )


        except Exception as exc:
            log.exception(
                msg = f'Error occured when processing Device Model {device_model} for manufacturer {manufacturer}. [{exc}]'
            )



def migrate_itam_operatingsystem_publisher(publisher, company, log, user):

    OperatingSystem = apps.get_model(
        app_label = 'itam',
        model_name = 'operatingsystem'
    )

    for operating_system in OperatingSystem.objects.filter( publisher_old = publisher ):

        try:

            type(operating_system).context.update({
                'logger': log,
                operating_system._meta.model_name: user
            })
            operating_system.publisher = company
            operating_system.save()

            operating_system.publisher_old = None
            operating_system.save()

            log.info(
                msg = f'Migrated Operating System {operating_system} to use company {company}'
            )


        except Exception as exc:
            log.exception(
                msg = f'Error occured when processing Operating System {operating_system} for manufacturer {publisher}. [{exc}]'
            )




def migrate_itam_software_publisher(publisher, company, log, user):

    Software = apps.get_model(
        app_label = 'itam',
        model_name = 'software'
    )

    for software in Software.objects.filter( publisher_old = publisher ):

        try:

            type(software).context.update({
                'logger': log,
                software._meta.model_name: user
            })
            software.publisher = company
            software.save()

            software.publisher_old = None
            software.save()

            log.info(
                msg = f'Migrated Software {software} to use company {company}'
            )


        except Exception as exc:
            log.exception(
                msg = f'Error occured when processing Software {software} for manufacturer {publisher}. [{exc}]'
            )




@receiver(post_migrate, dispatch_uid="manufacturer_to_company")
def manufacturer_to_company(sender, **kwargs):


    if sender.label != 'core':
        return

    log: CenturionLogger = settings.CENTURION_LOG.getChild( suffix = 'migration' ).getChild( suffix = 'core' )

    try:

        Manufacturer = apps.get_model(
            app_label = 'core',
            model_name = 'manufacturer'
        )

        ManufacturerAuditHistory = apps.get_model(
            app_label = 'core',
            model_name = str( Manufacturer().get_history_model_name() ).lower()
        )

        ManufacturerCenturionModelNote = apps.get_model(
            app_label = 'core',
            model_name = str( f'{Manufacturer._meta.object_name}CenturionModelNote' ).lower()
        )

        Company = apps.get_model(
            app_label = 'access',
            model_name = 'company'
        )

        CompanyAuditHistory = apps.get_model(
            app_label = 'access',
            model_name = str( Company().get_history_model_name() ).lower()
        )

        CompanyCenturionModelNote = apps.get_model(
            app_label = 'access',
            model_name = str( f'{Company._meta.object_name}CenturionModelNote' ).lower()
        )


        system_user = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(
            username = 'system'
        ).first()



        Company.context.update({
            'logger': log,
            Company._meta.model_name: system_user
        })


        # find all manufacturers, excluding names in companies
        company_names: list [ str ] = []
        for company in Company.objects.all():

            if company.name not in company_names:
                company_names += [ company.name ]


        manufacturers = Manufacturer.objects.exclude( name__in = company_names )

        for manufacturer in manufacturers:

            try:

                company = Company.objects.create(
                    organization = manufacturer.organization,
                    name = manufacturer.name,
                    model_notes = manufacturer.model_notes,
                )

                content_type = ContentType.objects.get(
                    app_label = company._meta.app_label,
                    model = company._meta.model_name
                )

                for history in ManufacturerAuditHistory.objects.filter(model = manufacturer):

                    company_history = CompanyAuditHistory()
                    company_history.organization = history.organization
                    company_history.centurionaudit_ptr = history.centurionaudit_ptr
                    company_history.model = company
                    company_history.action = history.action
                    company_history.user = history.user
                    company_history.content_type = content_type
                    company_history.created = history.created

                    company_history._state.adding = False

                    company_history.save()


                    log.info(
                        msg = f'Migrated Manufacturer {manufacturer} Audit History (id={history.id}) to Company {company} AuditHistory (id={company_history.id}).'
                    )

                    history.delete( keep_parents = True )

                    log.info(
                        msg = f'Removed Manufacturer {manufacturer} Audit History (id={history.id}).'
                    )


                for note in ManufacturerCenturionModelNote.objects.filter(model = manufacturer):

                    company_note = CompanyCenturionModelNote()
                    company_note.organization = note.organization
                    company_note.created = note.created
                    company_note.modified = note.modified
                    company_note.body = note.body
                    company_note.content_type = content_type
                    company_note.created_by = note.created_by
                    company_note.modified_by = note.modified_by
                    company_note.centurionmodelnote_ptr = note.centurionmodelnote_ptr
                    company_note.model = company

                    company_note._state.adding = False

                    company_note.save()


                    log.info(
                        msg = f'Migrated Manufacturer {manufacturer} Note (id={history.id}) to Company {company} Note (id={company_note.id}).'
                    )

                    company_note.delete( keep_parents = True )

                    log.info(
                        msg = f'Removed Manufacturer {manufacturer} Note (id={history.id}) .'
                    )


                log.info(
                    msg = f'Created Company {company} from Manufacturer {manufacturer}.'
                )

                migrate_itam_devicemodel_manufacturer(
                    manufacturer, company, log,
                    system_user,
                )

                migrate_itam_operatingsystem_publisher(
                    manufacturer, company, log,
                    system_user,
                )

                migrate_itam_software_publisher(
                    manufacturer, company, log,
                    system_user,
                )

                manufacturer.delete()

                log.info(
                    msg = f'Removed migrated manufacturer {manufacturer}.'
                )


            except Exception as exc:
                log.exception(
                    msg = f'Error occure when processing manufacturer {manufacturer}. [{exc}]'
                )


        print(f'Completed processing current Manufacturers migration to Comapny.')

    except Exception as exc:
        pass
