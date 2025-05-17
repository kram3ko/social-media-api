from rest_framework import serializers

from accounts.serializers import UserSerializer
from follows.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["follower", "followed", "liked_at"]
        read_only_fields = ["liked_at", "follower"]


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["followed"]

    def validate(self, attrs):
        follower = attrs.get("follower")
        followed = attrs.get("followed")
        print(f"Follower: {follower}, Followed: {followed}")
        if follower == followed:
            raise serializers.ValidationError("You cant follow yourself.")

        if Follow.objects.filter(follower=follower, followed=followed).exists():
            raise serializers.ValidationError("You are already following this user.")

        return attrs
