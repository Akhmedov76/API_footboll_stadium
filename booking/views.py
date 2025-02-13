from rest_framework import viewsets, permissions

from booking.models import Booking
from booking.serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, "role", None)

        if role == "admin" or role == "manager":
            return Booking.objects.all()
        return Booking.objects.filter(user=user)
