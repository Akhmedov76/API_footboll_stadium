from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from booking.models import Booking
from footboll_field.models import FootballField
from footboll_stadium.models import FootballStadium
from footboll_stadium.serializers import FootballStadiumSerializer
from utils.geo_near import calculate_distance


class FootballStadiumViewSet(viewsets.ModelViewSet):
    queryset = FootballStadium.objects.all()
    serializer_class = FootballStadiumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff and self.request.user.role != "manager":
            return Response({"error": "Only managers can create stadiums."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def available_fields(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')

        # Base queryset
        fields = FootballField.objects.all()

        # Filter by time availability
        if start_time and end_time:
            booked_fields = Booking.objects.filter(
                Q(start_time__lte=end_time) & Q(end_time__gte=start_time)
            ).values_list('field_id', flat=True)
            fields = fields.exclude(id__in=booked_fields)

        # Sort by distance if coordinates provided
        # if lat and lon:
        #     fields = fields.annotate(
        #         distance=ExpressionWrapper(
        #             (F('latitude') - float(lat)) ** 2 +
        #             (F('longitude') - float(lon)) ** 2,
        #             output_field=FloatField()
        #         )
        #     ).order_by('distance')

        serializer = self.get_serializer(fields, many=True)
        return Response(serializer.data)


class NearlyStadionField(viewsets.ModelViewSet):
    serializer_class = FootballStadiumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.latitude or not user.longitude:
            return FootballStadium.objects.none()

        nearby_stadions = []
        for stadion in FootballStadium.objects.all():
            distance = calculate_distance(stadion.latitude, stadion.longitude, user.latitude, user.longitude)

            if distance <= 50:
                nearby_stadions.append(stadion.id)
        # print(nearby_stadions)
        # print(user.latitude, user.longitude)
        # print(distance)
        return FootballStadium.objects.filter(id__in=nearby_stadions)
