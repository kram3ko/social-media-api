from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import (
    PostViewSet,
    LikePostView,
    CommentListCreateView,
    PostCreateView,
)

app_name = "posts"

router = DefaultRouter()

router.register("posts", PostViewSet, basename="posts")
urlpatterns = [
    path("", include(router.urls)),
    path("create/", PostCreateView.as_view(), name="create-post"),
    path("<int:post_id>/like/", LikePostView.as_view(), name="like-post"),
    path(
        "<int:post_id>/comments/",
        CommentListCreateView.as_view(),
        name="post-comments",
    ),
]
