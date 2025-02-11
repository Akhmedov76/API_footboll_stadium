from rest_framework import viewsets, permissions

from booking.models import Booking
from booking.serializers import BookingSerializer
from utils.geo_near import get_nearest_fields


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


from rest_framework.views import APIView
from rest_framework.response import Response


class NearestFieldsView(APIView):
    def get(self, request):
        user_lat = float(request.GET.get('lat'))
        user_lon = float(request.GET.get('lon'))

        fields = get_nearest_fields(user_lat, user_lon)
        data = [
            {"id": field.id, "name": field.name, "address": field.address, "distance": field.distance}
            for field in fields[:10]
        ]
        return Response(data)
