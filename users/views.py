import asyncio

from django.contrib.auth.hashers import make_password
from django.db import connection
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.geolocations import get_coordinates_from_address
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Define permissions for different actions.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Filter users based on the users role and permissions.
        """
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        elif getattr(user, "role", None) == "manager":
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_serializer_class(self):
        """
        Use the serializer class to create instances
        """
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer


class UserView(APIView):
    """
    View for managing users.
    """

    def get(self, request):
        """
        Get all users
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, first_name, last_name, email, role, phone, address, status FROM users_user",
            )
            columns = [col[0] for col in cursor.description]
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(users, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new user for user profile
        """
        data = request.data
        username = data.get("username")
        password = data.get("password")

        role = data.get("role", "user")
        phone = data.get("phone", "")
        address = data.get("address", "")
        status_user = data.get("status", "active")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email", "")
        is_superuser = data.get("is_superuser", False)
        is_active = data.get("is_active", True)
        is_staff = data.get("is_staff", False)

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users_user WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)

        coordinate = asyncio.run(get_coordinates_from_address(address))
        # print(coordinate)
        if coordinate:
            latitude, longitude = coordinate

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users_user 
                (username, password, first_name, last_name, email, role, phone, address, status, latitude, longitude, is_superuser ,is_active, is_staff, date_joined)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """, [
                username, hashed_password, first_name, last_name, email, role, phone, address, status_user,
                latitude, longitude, is_superuser, is_active, is_staff
            ])
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """
        Update user profile by user_id
        """
        data = request.data
        password = data.get("password")

        if password:
            hashed_password = make_password(password)

            with connection.cursor() as cursor:
                cursor.execute("""
                        UPDATE users_user SET password=%s WHERE id=%s
                    """, [hashed_password, pk])

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Delete user profile by user_id
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                    DELETE FROM users_user WHERE id=%s
                """, [pk])

        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
