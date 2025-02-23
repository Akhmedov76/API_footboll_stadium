from django.urls import path, include
from rest_framework.routers import DefaultRouter
from footboll_field.views import FootballFieldViewSet

router = DefaultRouter()
router.register(r'fields', FootballFieldViewSet, basename='field')

urlpatterns = [
    path('', include(router.urls)),
]
