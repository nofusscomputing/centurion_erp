from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelRetrieveUpdateViewSet

from settings.serializers.user_settings import (
    UserSettings,
    UserSettingsModelSerializer,
    UserSettingsViewSerializer
)



@extend_schema_view(
    # create=extend_schema(
    #     summary = 'Create an user setting',
    #     description="""Add a new device to the ITAM database.
    #     If you attempt to create a device and a device with a matching name and uuid or name and serial number
    #     is found within the database, it will not re-create it. The device will be returned within the message body.
    #     """,
    #     responses = {
    #         201: OpenApiResponse(description='Device created', response=UserSettingsViewSerializer),
    #         400: OpenApiResponse(description='Validation failed.'),
    #         403: OpenApiResponse(description='User is missing create permissions'),
    #     }
    # ),
    # destroy = extend_schema(
    #     summary = 'Delete an user setting',
    #     description = '',
    #     responses = {
    #         204: OpenApiResponse(description=''),
    #         403: OpenApiResponse(description='User is missing delete permissions'),
    #     }
    # ),
    # list = extend_schema(
    #     summary = 'Fetch all user settings',
    #     description='',
    #     responses = {
    #         200: OpenApiResponse(description='', response=UserSettingsViewSerializer),
    #         403: OpenApiResponse(description='User is missing view permissions'),
    #     }
    # ),
    retrieve = extend_schema(
        summary = 'Fetch user settings',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=UserSettingsViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an user setting',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=UserSettingsViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelRetrieveUpdateViewSet):

    model = UserSettings

    # filterset_fields = [
    #     'cluster',
    #     'devices',
    #     'software',
    # ]


    def get_serializer_class(self):

        if self.serializer_class is not None:

            return self.serializer_class


        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class
