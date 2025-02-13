from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from footboll_field.models import FootballField
from footboll_field.serializers import FootballFieldSerializer


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
