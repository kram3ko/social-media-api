from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from base.generics import GenericAPIView, ListCreateAPIView, CreateAPIView
from base.mixins import ListModelMixin
from base.viewsets import GenericViewSet
from posts.filters import PostFilter
from posts.models import Post, Like, Comment
from posts.serializers import (
    PostSerializer,
    LikeSerializer,
    PostCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)

from posts.tasks import publish_schedule_post


class PostViewSet(ListModelMixin, GenericViewSet):
    """List and retrieve posts. The list will show posts from users that
     the authenticated user follows."""
    request_serializer_class = PostSerializer
    response_serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PostFilter
    ordering_fields = ["created_at"]
    search_fields = ["post"]

    def get_queryset(self):
        user = self.request.user
        followed_ids = user.followed.values_list("followed_id", flat=True)
        return Post.objects.filter(user__in=list(followed_ids) + [user.id])


class PostCreateView(CreateAPIView):
    """
    Create a post. If schedule_date is provided, the post will be scheduled for that date.
    """
    request_serializer_class = PostCreateSerializer
    response_serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        schedule_date = serializer.validated_data.get("schedule_date")
        if schedule_date:
            instance = serializer.save(user=self.request.user, published=False)
            publish_schedule_post.apply_async(
                args=[instance.id],
                eta=schedule_date,
            )
        else:
            instance = serializer.save(
                user=self.request.user,
                published_at=timezone.now(),
            )
        return instance


class LikePostView(GenericAPIView):
    """Like or unlike a post If the post is already liked, it will be unliked."""
    request_serializer_class = LikeSerializer
    response_serializer_class = LikeSerializer

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {"detail": "You have already liked this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response_serializer = self.get_response_serializer(like)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response(
                {"detail": "Like successfully removed"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "You have not liked this post"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CommentListCreateView(ListCreateAPIView):
    request_serializer_class = CommentCreateSerializer
    response_serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)
        return serializer.instance
