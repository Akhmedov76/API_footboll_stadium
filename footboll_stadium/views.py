from datetime import datetime

from django.db import connection, DatabaseError
from django.utils.translation import gettext_lazy as _
from jsonschema.exceptions import ValidationError
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from footboll_stadium.models import FootballStadium
from footboll_stadium.serializers import FootballStadiumSerializer
from utils.geo_loc import get_distance
from utils.paginations import paginate_query


class FootballStadiumViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing football stadiums.
    """
    queryset = FootballStadium.objects.all()
    serializer_class = FootballStadiumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the stadium with the current user.
        """
        if not self.request.user.is_staff and self.request.user.role != "manager":
            return Response({"error": "Only managers can create stadiums."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Allow or deny access to list, create, update, partial_update and delete operations.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class NearlyStadionField(viewsets.ModelViewSet):
    """
    ViewSet for managing nearby football stadiums.
    """
    serializer_class = FootballStadiumSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get all nearby football stadiums within 50 km.
        """
        user = self.request.user

        if not user.latitude or not user.longitude:
            return FootballStadium.objects.none()

        nearby_stadions = []
        for stadion in FootballStadium.objects.all():
            point1 = (stadion.latitude, stadion.longitude,)
            point2 = (user.latitude, user.longitude,)
            distance = get_distance(point1, point2)
            if distance <= 50:
                nearby_stadions.append(stadion.id)
        print(nearby_stadions)

        return FootballStadium.objects.filter(id__in=nearby_stadions)


class StadiumViewSet(APIView):
    """
    Get a list all the stadiums
    """

    def get(self, request):
        """
        Get all active stadiums
        """
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')

        limit, offset = paginate_query(page, page_size)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, address, contact, status, owner_id FROM footboll_stadium_footballstadium "
                "WHERE status = 'active' LIMIT %s OFFSET %s", [limit, offset]
            )
            columns = [col[0] for col in cursor.description]
            stadiums = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(
            {"page": page, "page_size": page_size, "stadiums": stadiums},
            status=status.HTTP_200_OK,
        )

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


class GetNearbyStadium(APIView):
    """
    Get nearby stadiums based on user location
    """

    def get(self, request):
        user = request.user
        if not user.latitude or not user.longitude:
            return Response({"error": "User location not available."}, status=status.HTTP_400_BAD_REQUEST)

        page = request.GET.get('page')
        page_size = request.GET.get('page_size')

        limit, offset = paginate_query(page, page_size)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        s.id AS stadium_id, 
                        s.name AS stadium_name,
                        s.address AS address, 
                        s.contact AS contact, 
                        s.description AS description, 
                        s.latitude, 
                        s.longitude,
                        f.id AS field_id, 
                        f.name AS field_name, 
                        f.price_per_hour, 
                        f.working_hours_start, 
                        f.working_hours_end
                    FROM footboll_stadium_footballstadium s
                    JOIN footboll_field_footballfield f ON s.id = f.stadium_id
                    WHERE s.status = 'active'
                """, [limit, offset])

                columns = [col[0] for col in cursor.description]
                stadiums = [dict(zip(columns, row)) for row in cursor.fetchall()]

            nearby_stadiums = []
            for stadium in stadiums:
                point1 = (stadium['latitude'], stadium['longitude'])
                point2 = (user.latitude, user.longitude)
                distance = get_distance(point1, point2)
                distance_km = round(distance, 2)

                if distance_km <= 50:
                    nearby_stadiums.append(stadium)
            #################################################################################################################
            # nearby_stadiums = sorted(nearby_stadiums, key=lambda x: (                                                    ##
            #     get_distance((x['latitude'], x['longitude']), (user.latitude, user.longitude)), x['stadium_id']))        ##
            #################################################################################################################
            return Response({"page": page, "page_size": page_size, "Nearly stadion": nearby_stadiums},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except DatabaseError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetStadiumByFilterTime(APIView):
    """
    Get stadiums filtered by available time slots
    """

    def get(self, request):
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')

        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        limit, offset = paginate_query(page, page_size)

        if not start_time or not end_time:
            return Response({"error": "Start time and end time are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        s.id AS stadium_id, 
                        s.name AS stadium_name, 
                        s.latitude, 
                        s.longitude,
                        f.id AS field_id, 
                        f.name AS field_name, 
                        f.price_per_hour, 
                        f.working_hours_start, 
                        f.working_hours_end
                    FROM footboll_stadium_footballstadium s
                    JOIN footboll_field_footballfield f ON s.id = f.stadium_id
                    LEFT JOIN booking_booking b 
                        ON f.id = b.field_id 
                        AND (b.start_time > %s AND b.end_time > %s)  
                    WHERE s.status = 'active' AND b.id IS NULL, LIMIT %s OFFSET %s
                """, [end_time, start_time, limit, offset])

                columns = [col[0] for col in cursor.description]
                stadiums = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return Response({"page": page, "page_size": page_size, "stadiums": stadiums
                             }, status=status.HTTP_200_OK)

        except DatabaseError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
