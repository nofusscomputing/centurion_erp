import pytest
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models.organization import Organization

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from assistance.models.model_knowledge_base_article import KnowledgeBase, ModelKnowledgeBaseArticle

from itam.models.device import Device



class ModelKnowledgeBaseArticleModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = ModelKnowledgeBaseArticle

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        self.organization_two = Organization.objects.create(name='test_org_two')

        knowledge_base = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'title',
            content = 'sdfsdf'
        )

        self.knowledge_base = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'title two',
            content = 'sdfsdfdsf'
        )

        KnowledgeBase.objects.create(
            organization = self.organization_two,
            title = 'title two',
            content = 'sdfsdf'
        )

        self.device = Device.objects.create(
            organization = self.organization,
            name = 'device'
        )


        self.kwargs_item_create = {
            'article': knowledge_base,
            'model': str( self.device._meta.app_label ) + '.' + str( self.device._meta.model_name ),
            'model_pk': self.device.id
        }

        super().setUpTestData()



    def test_model_org_matches_model_org(self):
        """Test model clean function

        When an item is created, no org is supplied. The clean
        method within the model is responsible for setting the org
        to match the models org.
        """

        assert self.item.organization.id == self.device.organization.id



    def test_attribute_type_get_url(self):
        """Test field `<model>`type

        This testcase is a duplicate of a test with the same name.

        This model does not use nor require the `get_url` function.

        Attribute `get_url` must be str
        """

        assert type(self.item.get_url()) is not str


    def test_attribute_not_empty_get_url(self):
        """Test field `<model>` is not empty

        This testcase is a duplicate of a test with the same name.

        This model does not use nor require the `get_url` function.

        Attribute `get_url` must contain values
        """

        assert self.item.get_url() is None


    def test_create_validation_exception_no_organization(self):
        """ Tenancy objects must have an organization

        This test case is a duplicate of a test with the same name. this
        model does not require this test as the org is derived from the model.org

        Must not be able to create an item without an organization
        """

        pass


    def test_create_no_validation_exception_organization_match_model(self):
        """ Tenancy objects must have an organization

        Must not be able to create an item without an organization
        """

        kwargs_item_create = self.kwargs_item_create.copy()

        kwargs_item_create.update({
            'article': self.knowledge_base
        })

        del kwargs_item_create['organization']

        article = self.model.objects.create(
            **kwargs_item_create,
        )

        assert article.organization == self.organization
