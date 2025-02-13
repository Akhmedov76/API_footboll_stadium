from django.urls import path, include
from rest_framework.routers import DefaultRouter
from footboll_field.views import FootballFieldViewSet, NearlyStadionField

router = DefaultRouter()
router.register(r'football-fields', FootballFieldViewSet, basename='order')
router.register(r'nearby-fields', NearlyStadionField, basename='nearby-fields')

urlpatterns = [
    path('', include(router.urls)),
]
