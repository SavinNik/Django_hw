from rest_framework.permissions import IsAuthenticated
from advertisements.permissions import IsOwnerOrReadOnly, IsAllowAny
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.filters import AdvertisementFilter
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsOwnerOrReadOnly]
        elif self.action == ["list", "retrieve"]:
            permission_classes = [IsAllowAny]
        else:
            permission_classes = self.permission_classes
        
        return [permission() for permission in permission_classes]

