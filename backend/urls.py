from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'fields', views.FootballFieldViewSet)
router.register(r'bookings', views.BookingViewSet, basename='booking')
urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), ]
