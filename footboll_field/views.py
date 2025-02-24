from django.db import connection
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FootballField
from .serializers import FootballFieldSerializer


class FootballFieldViewSet(viewsets.ModelViewSet):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff and user.role != "manager":
            return FootballField.objects.filter(is_active=True)
        return FootballField.objects.all()


""" 
Use this method to create a new model 
"""


class FootballFieldView(APIView):

    def get(self, request):
        """
        Get all football fields
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, stadium_id, image, price_per_hour, status, created_at, updated_at, "
                "working_hours_start, working_hours_end FROM footboll_field_footballfield WHERE status = 'active'"
            )
            columns = [col[0] for col in cursor.description]
            football_fields = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(football_fields, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new football field
        """
        data = request.data
        name = data.get("name")
        stadium_id = data.get("stadium_id")
        image = data.get("image", "")
        price_per_hour = data.get("price_per_hour")
        status = data.get("status", "active")
        working_hours_start = data.get("working_hours_start", "09:00")
        working_hours_end = data.get("working_hours_end", "18:00")
        created_at = data.get("created_at", "")
        updated_at = data.get("updated_at", "")

        if not stadium_id:
            return Response({"error": "Stadium ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO footboll_field_footballfield (name, stadium_id, image, price_per_hour, status, working_hours_start, working_hours_end, created_at, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                [name, stadium_id, image, price_per_hour, status, working_hours_start, working_hours_end, created_at,
                 updated_at]
            )
            football_field_id = cursor.fetchone()[0]
        return Response({"id": football_field_id, "message": "Field created successfully"},
                        status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """
        Update a football field
        """
        data = request.data
        name = data.get("name", "")
        stadium_id = data.get("stadium_id", "")
        image = data.get("image", "")
        price_per_hour = data.get("price_per_hour", "")
        status = data.get("status", "")
        working_hours_start = data.get("working_hours_start", "")
        working_hours_end = data.get("working_hours_end", "")
        created_at = data.get("created_at", "")
        updated_at = data.get("updated_at", "")

        if not stadium_id:
            return Response({"error": "Stadium ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE footboll_field_footballfield SET name=%s, stadium_id=%s, image=%s, price_per_hour=%s, status=%s, working_hours_start=%s, working_hours_end=%s, created_at=%s, updated_at=%s WHERE id=%s RETURNING id",
                [name, stadium_id, image, price_per_hour, status, working_hours_start, working_hours_end, created_at,
                 updated_at, pk]
            )
            football_field_id = cursor.fetchone()[0]
            if football_field_id is None:
                return Response({"error": "Field not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"id": football_field_id, "message": "Field updated successfully"},
                        status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Delete a football field
        """
        with connection.cursor() as cursor:
            cursor.execute("UPDATE footboll_field_footballfield SET status='inactive' WHERE id=%s", [pk])

        return Response({"message": "Field deleted successfully"}, status=status.HTTP_200_OK)
