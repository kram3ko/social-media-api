from django.urls import path, include
from rest_framework.routers import DefaultRouter

from post.views import PostCreateListViewSet

app_name = "post"

router = DefaultRouter()

router.register("post", PostCreateListViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
