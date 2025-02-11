from django.utils.dateparse import parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from booking.serializers import BookingSerializer
from footboll_field.models import FootballField
from footboll_field.serializers import FootballFieldSerializer
from rest_framework.response import Response
from utils.geo_near import get_nearest_fields


class FootballFieldViewSet(viewsets.ModelViewSet):
    serializer_class = FootballFieldSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price_per_hour']
    search_fields = ['name', 'address']
    ordering_fields = ['price_per_hour', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return FootballField.objects.all()
        elif user.role == "manager":
            return FootballField.objects.filter(owner=user)
        return FootballField.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def nearest(self, request):
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")

        if not lat or not lon:
            return Response({"error": "Latitude and longitude are required"}, status=400)

        try:
            user_location = Point(float(lon), float(lat), srid=4326)
        except ValueError:
            return Response({"error": "Invalid latitude or longitude format"}, status=400)

        fields = FootballField.objects.annotate(
            distance=Distance(Point("longitude", "latitude", srid=4326), user_location)
        ).order_by("distance")[:10]

        data = FootballFieldSerializer(fields, many=True).data
        return Response(data)

    @action(detail=False, methods=['get'])
    def available_fields(self, request):
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")

        if not start_time or not end_time:
            return Response({"error": "Start time and end time are required"}, status=400)

        start_time = parse_datetime(start_time)
        end_time = parse_datetime(end_time)

        if not start_time or not end_time:
            return Response({"error": "Invalid datetime format"}, status=400)

        booked_fields = FootballField.objects.filter(
            bookings__start_time__lt=end_time,
            bookings__end_time__gt=start_time,
            bookings__status="CONFIRMED"
        ).distinct()

        available_fields = FootballField.objects.exclude(id__in=booked_fields.values_list("id", flat=True))

        data = FootballFieldSerializer(available_fields, many=True).data
        return Response(data)
