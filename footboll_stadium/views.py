from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response

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
