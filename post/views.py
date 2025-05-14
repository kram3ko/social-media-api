from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from base.filters import PostFilter
from base.mixins import BaseViewSetMixin
from post.models import Post
from post.serializers import PostSerializer


class PostCreateListViewSet(
    BaseViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_queryset(self):
        user = self.request.user
        followed_ids = user.following.values_list("followed_id", flat=True)
        return Post.objects.filter(user__in=list(followed_ids) + [user.id])
