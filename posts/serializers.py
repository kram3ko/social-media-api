from rest_framework import serializers

from accounts.serializers import UserSerializer
from posts.models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "post",
            "image",
            "created_at",
            "schedule_date",
            "published",
            "published_at",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    schedule_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ["post", "image", "schedule_date"]


class LikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["user", "post", "liked_at"]


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["post"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "post", "comment", "created_at", "updated_at"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment"]
