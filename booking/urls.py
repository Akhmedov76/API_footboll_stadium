from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, confirm_booking

router = DefaultRouter()
router.register(r'booking', BookingViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('booking/<int:booking_id>/confirm/', confirm_booking, name='confirm-booking'),
]
