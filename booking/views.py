from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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


def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.confirm()
    return HttpResponse("Booking has been confirmed!")
