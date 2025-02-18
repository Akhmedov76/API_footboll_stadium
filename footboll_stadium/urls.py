from django.urls import path, include
from rest_framework.routers import DefaultRouter
from footboll_stadium.views import FootballFieldViewSet, NearlyStadionField

router = DefaultRouter()
router.register(r'Stadium', FootballFieldViewSet, basename='order')
router.register(r'nearby-stadiums', NearlyStadionField, basename='nearby-stadium')

urlpatterns = [
    path('', include(router.urls)),
]
