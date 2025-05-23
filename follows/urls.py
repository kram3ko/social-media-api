from django.urls import path, include
from rest_framework.routers import DefaultRouter

from follows.views import FollowsViewSet

app_name = "follows"
router = DefaultRouter()
router.register("follows", FollowsViewSet, basename="follows")

urlpatterns = [
    path("", include(router.urls)),
]
