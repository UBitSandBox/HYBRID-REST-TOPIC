from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Config
from .serializers import ConfigSerializer

from ..permissions import ConfigRight


class ConfigViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    and `destroy` actions.

    Additionally we also provide an extra `current` action.

    * Requires token authentication.
    * Only member of config group are able to access this view.
    """

    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = (IsAuthenticated, ConfigRight)

    @action(detail=False)
    def current(self, request, *args, **kwargs):
        config = Config.objects.latest('id')
        serializer = ConfigSerializer(config)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
