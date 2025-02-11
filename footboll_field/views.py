from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action

from backend.permissions import IsOwnerOrReadOnly
from booking.serializers import BookingSerializer
from footboll_field.models import FootballField
from footboll_field.serializers import FootballFieldSerializer
from rest_framework.response import Response


class FootballFieldViewSet(viewsets.ModelViewSet):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price_per_hour']
    search_fields = ['name', 'address']
    ordering_fields = ['price_per_hour', 'created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        field = self.get_object()
        bookings = field.bookings.filter(status='CONFIRMED')
        return Response(BookingSerializer(bookings, many=True).data)
