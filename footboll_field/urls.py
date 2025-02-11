from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FootballFieldViewSet

router = DefaultRouter()
router.register(r'footboll_field', FootballFieldViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
