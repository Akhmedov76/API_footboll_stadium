from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, FootballField, Booking
from .serializers import UserSerializer, FootballFieldSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly, IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


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


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin():
            return Booking.objects.all()
        elif self.request.user.is_owner():
            return Booking.objects.filter(field__owner=self.request.user)
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
