import django.db.models.deletion
import django.utils.timezone
import json

from django.conf import settings
from django.contrib.auth.models import ContentType
from django.db import migrations, models

from access.models.organization_history import Tenant, OrganizationHistory
from access.models.team_history import Team, TeamHistory

from assistance.models.knowledge_base_history import KnowledgeBase, KnowledgeBaseHistory
from assistance.models.knowledge_base_category_history import KnowledgeBaseCategory, KnowledgeBaseCategoryHistory

from config_management.models.config_groups_history import ConfigGroups, ConfigGroupsHistory
from config_management.models.config_groups_hosts_history import ConfigGroupHosts, ConfigGroupHostsHistory
from config_management.models.config_groups_software_history import ConfigGroupSoftware, ConfigGroupSoftwareHistory

from core.models.history import History
from core.models.manufacturer_history import Manufacturer, ManufacturerHistory

from itam.models.device_history import Device, DeviceHistory
from itam.models.device_model_history import DeviceModel, DeviceModelHistory
from itam.models.device_operating_system_history import DeviceOperatingSystem, DeviceOperatingSystemHistory
from itam.models.device_software_history import DeviceSoftware, DeviceSoftwareHistory
from itam.models.device_type_history import DeviceType, DeviceTypeHistory
from itam.models.operating_system_history import OperatingSystem, OperatingSystemHistory
from itam.models.operating_system_version_history import OperatingSystemVersion, OperatingSystemVersionHistory
from itam.models.software_history import Software, SoftwareHistory
from itam.models.software_category_history import SoftwareCategory, SoftwareCategoryHistory
from itam.models.software_version_history import SoftwareVersion, SoftwareVersionHistory

from itim.models.cluster_history import Cluster, ClusterHistory
from itim.models.cluster_type_history import ClusterType, ClusterTypeHistory
from itim.models.port_history import Port, PortHistory
from itim.models.service_history import Service, ServiceHistory

from project_management.models.project_history import Project, ProjectHistory
from project_management.models.project_milestone_history import ProjectMilestone, ProjectMilestoneHistory
from project_management.models.project_state_history import ProjectState, ProjectStateHistory
from project_management.models.project_type_history import ProjectType, ProjectTypeHistory

from settings.models.external_link_history import ExternalLink, ExternalLinkHistory



def move_history(apps, schema_editor):

    print('')
    print(f"migtating history data to new history tables.....")

    model_history = History.objects.all().order_by('pk')    # Select ALL and order by oldest first

    for old_entry in model_history:

        print(f'    Starting migration of pk-{str(old_entry.pk)}')

        before = old_entry.before
        after = old_entry.after

        if(
            type(before) is str
            and before != '{}'
        ):

            before = json.loads(before)

        elif before == '{}':

            before:dict = {}


        if(
            type(after) is str
            and after != '{}'
        ):

            after = json.loads(after)

        elif after == '{}':

            after:dict = {}



        new_history_model = None

        item_details = model_details(
            item_pk = old_entry.item_pk,
            item_class = old_entry.item_class
        )

        new_history_model = item_details['class']

        if item_details['object'] is not None:
                
            match item_details['object']._meta.model_name:

                case 'configgroups':

                    if old_entry.item_class == old_entry.item_parent_class:

                        old_entry.item_parent_pk = None
                        old_entry.item_parent_class = None


                case 'configgroupsoftware':

                    old_entry.item_parent_pk = item_details['object'].config_group.pk

                    old_entry.item_parent_class = item_details['object'].config_group._meta.model_name

                case 'operatingsystemversion':

                    old_entry.item_parent_pk = None
                    old_entry.item_parent_class = None

                case 'softwareversion':

                    old_entry.item_parent_pk = None
                    old_entry.item_parent_class = None

                case 'projectmilestone':

                    old_entry.item_parent_pk = None
                    old_entry.item_parent_class = None




        item_details_parent = None
        if(
            old_entry.item_parent_pk
            and item_details['class'] is not None
            and item_details['content'] is not None
            and item_details['object'] is not None
            and new_history_model._meta.model_name != 'team'
            and new_history_model._meta.model_name != 'teamhistory'
        ):

            item_details_parent = model_details(
                item_pk = old_entry.item_parent_pk,
                item_class = old_entry.item_parent_class
            )


        new_entry = None
        if item_details_parent is not None:

            new_entry = new_history_model.objects.create(
                organization = item_details_parent['object'].organization,
                before = before,
                after = after,
                action = old_entry.action,
                user = old_entry.user,
                created = old_entry.created,

                content_type = item_details_parent['content'],
                model = item_details_parent['object'],
                child_model = item_details['object'],
            )

        elif(
            item_details['class'] is not None
            and item_details['content'] is not None
            and item_details['object'] is not None
        ):


            organization = getattr(item_details['object'], 'organization', None)

            if item_details['object']._meta.model_name == 'organization':

                organization = item_details['object']


            new_entry = new_history_model.objects.create(
                organization = organization,
                before = before,
                after = after,
                action = old_entry.action,
                user = old_entry.user,
                created = old_entry.created,

                content_type = item_details['content'],
                model = item_details['object'],
            )

        else:

            print(f'      [Notice] Could not determine details, pk-{str(old_entry.pk)} not migrated')


        if new_entry is None:

            print(f'      [Failure] not migrated, pk-{str(old_entry.pk)}')

        elif new_entry is not None:

            print(f'      [Success] migrated history entry pk-{str(old_entry.pk)} to new history table pk{str(new_entry.pk)}')



class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_organizationhistory_teamhistory'),
        ('assistance', '0005_knowledgebasecategoryhistory_knowledgebasehistory'),
        ('config_management', '0007_configgroupshistory_configgrouphostshistory_and_more'),
        ('core', '0015_modelhistory_manufacturerhistory_and_more'),
        ('itam', '0009_devicehistory_devicemodelhistory_devicetypehistory_and_more'),
        ('itim', '0008_clusterhistory_clustertypehistory_porthistory_and_more'),
        ('project_management', '0005_projecthistory_projectmilestonehistory_and_more'),
        ('settings', '0011_appsettingshistory_externallinkhistory')
    ]

    operations = [
        migrations.RunPython(move_history),
    ]



def model_details(item_pk, item_class) -> dict:

    history_object = None
    history_class = None
    history_content = None

    model_class = None


    match item_class:

        case 'appsettings':

            pass

        case 'cluster':

            model_class = Cluster

            history_class = ClusterHistory

        case 'clustertype':

            model_class = ClusterType

            history_class = ClusterTypeHistory

        case 'configgrouphosts':

            model_class = ConfigGroupHosts

            history_class = ConfigGroupHostsHistory

        case 'configgroups':

            model_class = ConfigGroups

            history_class = ConfigGroupsHistory

        case 'configgroupsoftware':

            model_class = ConfigGroupSoftware

            history_class = ConfigGroupSoftwareHistory

        case 'device':

            model_class = Device

            history_class = DeviceHistory

        case 'devicemodel':

            model_class = DeviceModel

            history_class = DeviceModelHistory

        case 'deviceoperatingsystem':

            model_class = DeviceOperatingSystem

            history_class = DeviceOperatingSystemHistory


        case 'devicesoftware':

            model_class = DeviceSoftware

            history_class = DeviceSoftwareHistory

        case 'devicetype':

            model_class = DeviceType

            history_class = DeviceTypeHistory

        case 'externallink':

            model_class = ExternalLink

            history_class = ExternalLinkHistory

        case 'knowledgebase':

            model_class = KnowledgeBase

            history_class = KnowledgeBaseHistory

        case 'knowledgebasecategory':

            model_class = KnowledgeBaseCategory

            history_class = KnowledgeBaseCategoryHistory

        case 'manufacturer':

            model_class = Manufacturer

            history_class = ManufacturerHistory

        case 'operatingsystem':

            model_class = OperatingSystem

            history_class = OperatingSystemHistory

        case 'operatingsystemversion':

            model_class = OperatingSystemVersion

            history_class = OperatingSystemVersionHistory

        case 'organization':

            model_class = Tenant

            history_class = OrganizationHistory

        case 'port':

            model_class = Port

            history_class = PortHistory

        case 'project':

            model_class = Project

            history_class = ProjectHistory

        case 'projectmilestone':

            model_class = ProjectMilestone

            history_class = ProjectMilestoneHistory

        case 'projectstate':

            model_class = ProjectState

            history_class = ProjectStateHistory

        case 'projecttype':

            model_class = ProjectType

            history_class = ProjectTypeHistory

        case 'service':

            model_class = Service

            history_class = ServiceHistory

        case 'software':

            model_class = Software

            history_class = SoftwareHistory

        case 'softwarecategory':

            model_class = SoftwareCategory

            history_class = SoftwareCategoryHistory

        case 'softwareversion':

            model_class = SoftwareVersion

            history_class = SoftwareVersionHistory

        case 'team':

            model_class = Team

            history_class = TeamHistory


    if(
        model_class is not None
        and history_class is not None
    ):

        try:

            if history_object is None:

                history_object = model_class.objects.get(
                    pk = item_pk
                )

                history_content = ContentType.objects.get(
                    app_label = model_class._meta.app_label,
                    model = model_class._meta.model_name,
                )

        except model_class.DoesNotExist:

            print(f'    model {model_class._meta.model_name}-{str(item_pk)} does not exist')


    return {
        'class': history_class,
        'content': history_content,
        'object': history_object,
    }
