from django.utils.encoding import force_str

from rest_framework import serializers
from rest_framework_json_api.metadata import JSONAPIMetadata
from rest_framework.request import clone_request
from rest_framework.reverse import reverse
from rest_framework.utils.field_mapping import ClassLookupDict

from rest_framework_json_api.utils import get_related_resource_type

from app.serializers.user import User, UserBaseSerializer

from core import fields as centurion_field
from core.fields.badge import BadgeField
from core.fields.icon import IconField



class OverRideJSONAPIMetadata(JSONAPIMetadata):

    type_lookup = ClassLookupDict(
        {
            serializers.Field: "GenericField",
            serializers.RelatedField: "Relationship",
            serializers.BooleanField: "Boolean",
            serializers.CharField: "String",
            serializers.URLField: "URL",
            serializers.EmailField: "Email",
            serializers.RegexField: "Regex",
            serializers.SlugField: "Slug",
            serializers.IntegerField: "Integer",
            serializers.FloatField: "Float",
            serializers.DecimalField: "Decimal",
            serializers.DateField: "Date",
            serializers.DateTimeField: "DateTime",
            serializers.TimeField: "Time",
            serializers.ChoiceField: "Choice",
            serializers.MultipleChoiceField: "MultipleChoice",
            serializers.FileField: "File",
            serializers.ImageField: "Image",
            serializers.ListField: "List",
            serializers.DictField: "Dict",
            serializers.Serializer: "Serializer",
            serializers.JSONField: "JSON",    # New. Does not exist in base class
            BadgeField: 'Badge',
            IconField: 'Icon',
            User: 'Relationship',
            UserBaseSerializer: 'Relationship',
            centurion_field.CharField: 'String',
            centurion_field.MarkdownField: 'Markdown'
        }
    )



class ReactUIMetadata(OverRideJSONAPIMetadata):


    def determine_metadata(self, request, view):

        metadata = {}

        metadata["name"] = view.get_view_name()

        metadata["description"] = view.get_view_description()

        if 'pk' in view.kwargs:

            if view.kwargs['pk']:

                qs = view.get_queryset()[0]

                if hasattr(qs, 'get_url'):

                    metadata['return_url'] = qs.get_url( request )

        elif view.kwargs:

            metadata['return_url'] = reverse('v2:' + view.basename + '-list', request = view.request, kwargs = view.kwargs )

        else:

            metadata['return_url'] = reverse('v2:' + view.basename + '-list', request = view.request )


        metadata["renders"] = [
            renderer.media_type for renderer in view.renderer_classes
        ]

        metadata["parses"] = [parser.media_type for parser in view.parser_classes]

        metadata["allowed_methods"] = view.allowed_methods

        if hasattr(view, 'get_serializer'):
            serializer = view.get_serializer()
            metadata['fields'] = self.get_serializer_info(serializer)


        if view.suffix == 'Instance':

            metadata['layout'] = view.get_page_layout()


            if hasattr(view, 'get_model_documentation'):

                if view.get_model_documentation():

                    metadata['documentation'] = view.get_model_documentation()


        elif view.suffix == 'List':

            if hasattr(view, 'table_fields'):

                metadata['table_fields'] = view.get_table_fields()

            if view.documentation:

                metadata['documentation'] = view.documentation

            if hasattr(view, 'page_layout'):

                metadata['layout'] = view.get_page_layout()


        metadata['navigation'] = [
            {
                "display_name": "Access",
                "name": "access",
                "pages": [
                    {
                        "display_name": "Organization",
                        "name": "organization",
                        "link": "/access/organization"
                    }
                ]
            },
            {
                "display_name": "Assistance",
                "name": "assistance",
                "pages": [
                    {
                        "display_name": "Requests",
                        "name": "request",
                        "icon": "ticket_request",
                        "link": "/assistance/ticket/request"
                    },
                    {
                        "display_name": "Knowledge Base",
                        "name": "knowledge_base",
                        "icon": "information",
                        "link": "/assistance/knowledge_base"
                    }
                ]
            },
            {
                "display_name": "ITAM",
                "name": "itam",
                "pages": [
                    {
                        "display_name": "Devices",
                        "name": "device",
                        "icon": "device",
                        "link": "/itam/device"
                    },
                    {
                        "display_name": "Operating System",
                        "name": "operating_system",
                        "link": "/itam/operating_system"
                    },
                    {
                        "display_name": "Software",
                        "name": "software",
                        "link": "/itam/software"
                    }
                ]
            },
            {
                "display_name": "ITIM",
                "name": "itim",
                "pages": [
                    {
                        "display_name": "Changes",
                        "name": "ticket_change",
                        "link": "/itim/ticket/change"
                    },
                    {
                        "display_name": "Clusters",
                        "name": "cluster",
                        "link": "/itim/cluster"
                    },
                    {
                        "display_name": "Incidents",
                        "name": "ticket_incident",
                        "link": "/itim/ticket/incident"
                    },
                    {
                        "display_name": "Problems",
                        "name": "ticket_problem",
                        "link": "/itim/ticket/problem"
                    },
                    {
                        "display_name": "Services",
                        "name": "service",
                        "link": "/itim/service"
                    },
                ]
            },
            {
                "display_name": "Config Management",
                "name": "config_management",
                "icon": "ansible",
                "pages": [
                    {
                        "display_name": "Groups",
                        "name": "group",
                        "icon": 'config_management',
                        "link": "/config_management/group"
                    }
                ]
            },
            {
                "display_name": "Project Management",
                "name": "project_management",
                "icon": 'project',
                "pages": [
                    {
                        "display_name": "Projects",
                        "name": "project",
                        "icon": 'kanban',
                        "link": "/project_management/project"
                    }
                ]
            },

            {
                "display_name": "Settings",
                "name": "settings",
                "pages": [
                    {
                        "display_name": "System",
                        "name": "setting",
                        "icon": "system",
                        "link": "/settings"
                    },
                    {
                        "display_name": "Task Log",
                        "name": "celery_log",
                        # "icon": "settings",
                        "link": "/settings/celery_log"
                    }
                ]
            }
        ]


        return metadata




    def get_field_info(self, field):
        """ Custom from `rest_framewarok_json_api.metadata.py`

        Require that read-only fields have their choices added to the 
        metadata.

        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = {}
        serializer = field.parent

        if hasattr(field, 'textarea'):

            if field.textarea:

                field_info["multi_line"] = True

        if isinstance(field, serializers.ManyRelatedField):
            field_info["type"] = self.type_lookup[field.child_relation]
        else:
            field_info["type"] = self.type_lookup[field]

        try:
            serializer_model = serializer.Meta.model
            field_info["relationship_type"] = self.relation_type_lookup[
                getattr(serializer_model, field.field_name)
            ]
        except KeyError:
            pass
        except AttributeError:
            pass
        else:
            field_info["relationship_resource"] = get_related_resource_type(field)

        if hasattr(field, 'autolink'):

            if field.autolink:

                field_info['autolink'] = field.autolink


        field_info["required"] = getattr(field, "required", False)


        if hasattr(field, 'style_class'):

            field_info["style"]: dict = {
                'class': field.style_class
            }


        attrs = [
            "read_only",
            "write_only",
            "label",
            "help_text",
            "min_length",
            "max_length",
            "min_value",
            "max_value",
            "initial",
        ]

        for attr in attrs:
            value = getattr(field, attr, None)
            if value is not None and value != "":
                field_info[attr] = force_str(value, strings_only=True)

        if getattr(field, "child", None):
            field_info["child"] = self.get_field_info(field.child)
        elif getattr(field, "fields", None):
            field_info["children"] = self.get_serializer_info(field)

        if (
            # not field_info.get("read_only")
            hasattr(field, "choices")
        ):
            field_info["choices"] = [
                {
                    "value": choice_value,
                    "display_name": force_str(choice_name, strings_only=True),
                }
                for choice_value, choice_name in field.choices.items()
            ]

        if (
            hasattr(serializer, "included_serializers")
            and "relationship_resource" in field_info
        ):
            field_info["allows_include"] = (
                field.field_name in serializer.included_serializers
            )

        return field_info