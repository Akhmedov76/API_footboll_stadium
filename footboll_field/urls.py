from django.urls import path, include
from rest_framework.routers import DefaultRouter

from footboll_field.views import FootballFieldViewSet, FootballFieldDetailView

router = DefaultRouter()
router.register(r'fields', FootballFieldViewSet, basename='field')
router.register(r'field/<int:pk>/', FootballFieldDetailView, basename='field-detail')

urlpatterns = [
    path('', include(router.urls)),
]
