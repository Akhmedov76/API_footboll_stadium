from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from footboll_stadium.models import FootballField
from footboll_stadium.serializers import FootballFieldSerializer
from utils.geo_near import calculate_distance


class FootballFieldViewSet(viewsets.ModelViewSet):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price_per_hour']
    search_fields = ['name', 'address']
    ordering_fields = ['price_per_hour', 'created_at']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, "role", None) == "manager":
            return FootballField.objects.all()
        return FootballField.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NearlyStadionField(viewsets.ModelViewSet):
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.latitude or not user.longitude:
            return FootballField.objects.none()

        nearby_stadions = []
        for stadion in FootballField.objects.all():
            distance = calculate_distance(stadion.latitude, stadion.longitude, user.latitude, user.longitude)

            if distance <= 50:
                nearby_stadions.append(stadion.id)
        # print(nearby_stadions)
        # print(user.latitude, user.longitude)
        # print(distance)
        return FootballField.objects.filter(id__in=nearby_stadions)
