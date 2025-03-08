from rest_framework import serializers

from devops.models.feature_flag import FeatureFlag



class ModelSerializer(
    serializers.ModelSerializer,
):


    class Meta:

        model = FeatureFlag

        fields =  [
            'id',
            'name',
            'description',
            'enabled',
            'created',
            'modified',
        ]

        read_only_fields = [
            'id',
            'name',
            'description',
            'enabled',
            'created',
            'modified',
        ]


    def to_representation(self, instance):

        key_id = str(instance.created.year) + '-' + str(f'{instance.id:05}')

        return {
            key_id : {
                "name": instance.name,
                "description": instance.description,
                "enabled": instance.enabled,
                "created": instance.created,
                "modeified": instance.modified
            }
        }
