from django.urls import path, include
from rest_framework.routers import DefaultRouter

from footboll_field.views import FootballFieldViewSet, FootballFieldView

router = DefaultRouter()
router.register(r'fields', FootballFieldViewSet, basename='field')

urlpatterns = [
    path('', include(router.urls)),
    path('v1-field/', FootballFieldView.as_view()),
]
