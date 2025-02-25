from datetime import datetime

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.models import Booking
from booking.serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the booking with the current user.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)


def confirm_booking(request, booking_id):
    """
    Confirm a booking
    """
    booking = get_object_or_404(Booking, id=booking_id)
    booking.confirm()
    return HttpResponse("Booking has been confirmed!")


class BookingsView(APIView):
    """
    get all bookings fields
    """

    def get(self, request, *args, **kwargs):
        """
        Get all bookings fields
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, field_id, user_id, start_time, end_time, status FROM booking_booking"
            )
            columns = [col[0] for col in cursor.description]
            bookings = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for booking in bookings:
            booking["start_time"] = booking["start_time"].strftime("%d.%m.%Y %H:%M:%S")
            booking["end_time"] = booking["end_time"].strftime("%d.%m.%Y %H:%M:%S")

        return Response(bookings, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new booking
        """
        data = request.data
        field_id = data.get("field_id")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        status = data.get("status", "pending")
        user_id = request.user.id
        created_at = data.get("created_at", "")
        updated_at = data.get("updated_at", "")

        if not field_id or not start_time or not end_time:
            return Response({"error": "Field ID, start time, and end time are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        start_time = [datetime.strptime(start_time, '%Y-%m-%dT%H:%M')]
        end_time = [datetime.strptime(end_time, '%Y-%m-%dT%H:%M')]

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO booking_booking (field_id, user_id, start_time, end_time, status, created_at, "
                           "updated_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW()) RETURNING id",
                           [field_id, user_id, start_time, end_time, status, created_at, updated_at]
                           )
            booking_id = cursor.fetchone()[0]

        return Response({"id": booking_id, "message": "Booking created successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request, booking_id):
        """
        Update a booking status
        """
        data = request.data
        status = data.get("status", "")

        if not status:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("UPDATE booking_booking SET status=%s, updated_at=NOW() WHERE id=%s", [status, booking_id])

        return Response({"message": "Booking status updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, booking_id):
        """
        Delete a booking
        """
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM booking_booking WHERE id=%s", [booking_id])

        return Response({"message": "Booking deleted successfully"}, status=status.HTTP_200_OK)
