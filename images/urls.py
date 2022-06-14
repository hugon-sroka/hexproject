from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)
from images.views import ImageViewSet

router = DefaultRouter()

router.register('recipes', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

