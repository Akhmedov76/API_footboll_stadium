from .models import FootballField
from .serializers import FootballFieldSerializer
from rest_framework import viewsets, permissions


class FootballFieldViewSet(viewsets.ModelViewSet):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.IsAuthenticated]


class FootballFieldDetailView(viewsets.ModelViewSet):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        field_id = self.kwargs.get('pk')
        return FootballField.objects.filter(id=field_id)
