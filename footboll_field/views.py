from django.db import connection
from rest_framework import viewsets, permissions
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
