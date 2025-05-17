from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response

from base.viewsets import ModelViewSet
from follows.models import Follow
from follows.serializers import FollowSerializer, FollowCreateSerializer

User = get_user_model()


class FollowsViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    request_serializer_class = FollowCreateSerializer
    response_serializer_class = FollowCreateSerializer

    response_action_serializer_classes = {
        "list": FollowSerializer,
    }

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
        return serializer.instance

    @action(detail=False, methods=["get"])
    def following(self, request):
        """Who I read. Show the users I follow"""
        queryset = Follow.objects.filter(follower=request.user)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def followers(self, request):
        """Who reads me Show the users that follow me"""
        queryset = Follow.objects.filter(followed=request.user)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)
