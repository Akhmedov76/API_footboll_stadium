from django.urls import path, include
from rest_framework.routers import DefaultRouter

from footboll_stadium.views import FootballStadiumViewSet, NearlyStadionField, StadiumViewSet, GetNearbyStadium

router = DefaultRouter()
router.register(r'Stadium', FootballStadiumViewSet, basename='order')
router.register(r'nearby-stadiums', NearlyStadionField, basename='nearby-stadium')

urlpatterns = [
    path('', include(router.urls)),
    path('v1-stadium/', StadiumViewSet.as_view()),
    path('v1-stadium/<int:pk>/', StadiumViewSet.as_view()),
    path('v1-nearby-stadiums/', GetNearbyStadium.as_view(), name='get-nearby-stadiums'),
    # path('nearby-stadiums/<float:latitude>/<float:longitude>/', GetNearbyStadium.as_view(), name='get-nearby-stadiums-by-location'),
]
