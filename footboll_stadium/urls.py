from django.urls import path, include
from rest_framework.routers import DefaultRouter

from footboll_stadium.views import FootballStadiumViewSet, NearlyStadionField, StadiumViewSet

router = DefaultRouter()
router.register(r'Stadium', FootballStadiumViewSet, basename='order')
router.register(r'nearby-stadiums', NearlyStadionField, basename='nearby-stadium')

urlpatterns = [
    path('', include(router.urls)),
    path('v1-stadium/', StadiumViewSet.as_view()),
]
