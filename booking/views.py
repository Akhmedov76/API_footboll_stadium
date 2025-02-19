from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from booking.models import Booking
from booking.serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.confirm()
    return HttpResponse("Booking has been confirmed!")
