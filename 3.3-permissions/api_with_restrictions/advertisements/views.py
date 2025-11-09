from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement, UserFavoriteAdvertisement
from .serializers import AdvertisementSerializer, UserFavoriteAdvertisementSerializer
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AdvertisementFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        """Получение набора данных для пользователя"""
        if self.request.user.is_authenticated:
            return self.queryset.filter(
                Q(status__in=['OPEN', 'CLOSED']) |
                Q(creator=self.request.user)
            )

        return self.queryset.exclude(status='DRAFT')
    
    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action in ["add_to_favorite", "favorite_advertisements"]:
            return [IsAuthenticated()]
        return []
    
    @action(detail=False, methods=['get'])
    def favorite_advertisements(self, request):
        favorite_advertisements = UserFavoriteAdvertisement.objects.filter(
            user=self.request.user
        ).select_related('advertisement')
        data=[]
        for adv in favorite_advertisements:
            data.append(adv.advertisement)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_to_favorite(self, request, pk=None):
        advertisement = self.get_object()
        data = {
            'advertisement': advertisement.id,
        }
        serializer = UserFavoriteAdvertisementSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Объявление добавлено в избранное'})
        return Response(serializer.errors, status=400)
