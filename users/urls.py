from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from utils import geolocations

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls')),
]
