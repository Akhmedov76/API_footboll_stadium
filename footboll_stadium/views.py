from pyexpat.errors import messages

from django.db import connection
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from footboll_stadium.models import FootballStadium
from footboll_stadium.serializers import FootballStadiumSerializer
from utils.geo_near import calculate_distance
from django.utils.translation import gettext_lazy as _


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


class StadiumViewSet(APIView):
    """
    Get a list all the stadiums
    """

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, address, contact, status, owner_id FROM footboll_stadium_footballstadium WHERE status = 'active'"
            )
            columns = [col[0] for col in cursor.description]
            stadiums = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(stadiums, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new stadium
        """

        data = request.data

        name = data.get("name")
        address = data.get("address")
        contact = data.get("contact", "")
        description = data.get("description", "")
        image = data.get("image", "")
        owner_id = data.get("owner_id")

        if not owner_id:
            return Response({"error": _("Owner ID is required.")}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO footboll_stadium_footballstadium (name, address, contact, description, image, owner_id, status,created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW()) RETURNING id
            """, [name, address, contact, description, image, owner_id, 'active'])
            stadium_id = cursor.fetchone()[0]
        return Response({"id": stadium_id, "messages": _("Stadium created successfully")},
                        status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """
        Update a stadium
        """
        data = request.data

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name, address, contact, image, description FROM footboll_stadium_footballstadium WHERE id=%s",
                [pk]
            )
            stadium = cursor.fetchone()
            if not stadium:
                return Response({"error": "Stadium not found"}, status=status.HTTP_404_NOT_FOUND)

            name = data.get("name", stadium[0])
            address = data.get("address", stadium[1])
            contact = data.get("contact", stadium[2])
            image = data.get("image", stadium[3])
            description = data.get("description", stadium[4])

            cursor.execute(
                """
                UPDATE footboll_stadium_footballstadium SET name=%s, address=%s, contact=%s, image=%s, description=%s, updated_at=NOW() WHERE id=%s
            """, [name, address, contact, image, description, pk])

        return Response({"message": _("Stadium updated successfully")}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM footboll_stadium_footballstadium WHERE id=%s
            """, [pk])
        return Response({"message": _("Stadium deleted successfully")}, status=status.HTTP_200_OK)


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

        return FootballStadium.objects.filter(id__in=nearby_stadions)
