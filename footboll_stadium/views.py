from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from footboll_stadium.models import FootballStadium
from footboll_stadium.serializers import FootballStadiumSerializer
from utils.geo_near import calculate_distance


class FootballFieldViewSet(viewsets.ModelViewSet):
    queryset = FootballStadium.objects.all()
    serializer_class = FootballStadiumSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price_per_hour']
    search_fields = ['name', 'address']
    ordering_fields = ['price_per_hour', 'created_at']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, "role", None) == "manager":
            return FootballStadium.objects.all()
        return FootballStadium.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
