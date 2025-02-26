from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, confirm_booking, BookingsView

"""
    Crate API routes for bookings
"""
router = DefaultRouter()
router.register(r'booking', BookingViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('booking/<int:booking_id>/confirm/', confirm_booking, name='confirm-booking'),
    path('v1/booking/', BookingsView.as_view(), name='bookings'),
    path('v1/booking/<int:booking_id>/', BookingsView.as_view()),
]
