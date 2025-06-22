from django.shortcuts import Http404
from django.views.generic import View


class FeatureFlagView(View):
    """Featur Flag View

    This view serves the purpose of being the stand-in view for a view that
    has been disabled via a feature flag.
    """

    def delete(self, request):

        raise Http404()

    def get(self, request):

        raise Http404()

    def head(self, request):

        raise Http404()

    def options(self, request):

        raise Http404()

    def patch(self, request):

        raise Http404()

    def post(self, request):

        raise Http404()

    def put(self, request):

        raise Http404()
