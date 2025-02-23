import hashlib

from openid.cryptutil import sha256
from rest_framework import viewsets, permissions
from social_core.utils import first
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        elif getattr(user, "role", None) == "manager":
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer


class UserView(APIView):

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, first_name, last_name, email, role, phone, address, status FROM users_user",
            )
            columns = [col[0] for col in cursor.description]
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(users, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users_user WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)

        role = data.get("role", "user")
        phone = data.get("phone", "")
        address = data.get("address", "")
        status_user = data.get("status", "active")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email", "")

        with connection.cursor() as cursor:
            cursor.execute("""
                    INSERT INTO users_user (username, password, first_name, last_name, email, role, phone, address, status, date_joined, is_superuser, is_staff, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s) RETURNING id
                """, [username, hashed_password, first_name, last_name, email, role, phone, address, status_user, False,
                      False,
                      True])
            user_id = cursor.fetchone()[0]

        return Response({"id": user_id, "message": "User created successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
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
        with connection.cursor() as cursor:
            cursor.execute("""
                    DELETE FROM users_user WHERE id=%s
                """, [pk])

        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
