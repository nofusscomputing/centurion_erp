from rest_framework import serializers

from access.serializers.organization import Organization, TenantBaseSerializer

from api.serializers import common

from core import exceptions as centurion_exceptions

from devops.models.feature_flag import FeatureFlag

from itam.serializers.software import Software, SoftwareBaseSerializer


class OrganizationField(common.OrganizationField):

    def get_queryset(self):

        qs = super().get_queryset()

        qs = qs.filter(id__in = list(Organization.objects.filter(
            software__feature_flagging__enabled = True
        ).distinct().values_list('software__feature_flagging__organization', flat = True)))

        return qs



class SoftwareField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):

        qs = Software.objects.filter(
            feature_flagging__enabled = True
        ).distinct()

        return qs



class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:devops:_api_v2_feature_flag-detail", format="html"
    )


    class Meta:

        model = FeatureFlag

        fields = [
            'id',
            'display_name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'url',
        ]


class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):

    organization = OrganizationField(required = True)

    software = SoftwareField(required = True, write_only = True)

    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = FeatureFlag

        note_basename = 'devops:_api_v2_feature_flag_note'

        fields =  [
            'id',
            'organization',
            'display_name',
            'software',
            'name',
            'description',
            'enabled',
            'model_notes',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]


    def is_valid(self, raise_exception = False):

        valid_software_orgs = []

        software = self.initial_data.get('software', None)

        organization = self.initial_data.get('organization', None)

        if getattr(self, 'instance', None):

            software = self.instance.software.id

            organization = self.instance.organization.id


        if(
            software is not None
            and organization is not None
        ):

            valid_software_orgs = Software.objects.filter(
                feature_flagging__enabled = True,
                feature_flagging__software_id = int(software)
            ).distinct().values_list(
                'feature_flagging__organization',
                flat = True
            )


            if len(valid_software_orgs) == 0:

                raise centurion_exceptions.ValidationError(
                    detail = {
                        'software': 'Software not enabled for Feature flagging'
                    },
                    code = 'feature_flagging_disabled'
                )

            if int(organization) not in valid_software_orgs:

                raise centurion_exceptions.ValidationError(
                    detail = {
                        'organization': 'Feature flagging not enabled for this software within this organization'
                    },
                    code = 'feature_flagging_wrong_organizaiton'
                )

        is_valid = super().is_valid( raise_exception = raise_exception )

        return is_valid




class ViewSerializer(ModelSerializer):

    organization = TenantBaseSerializer( read_only = True )

    software = SoftwareBaseSerializer( read_only = True )
