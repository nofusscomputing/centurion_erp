import pytest

from core.models.audit import AuditMetaModel



@pytest.fixture( scope = 'class')
def model(model_centurionauditmeta):

    yield model_centurionauditmeta


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_centurionauditmeta):

    request.cls.kwargs_create_item = kwargs_centurionauditmeta.copy()

    yield kwargs_centurionauditmeta.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
