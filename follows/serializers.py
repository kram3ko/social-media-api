from rest_framework import serializers

from accounts.serializers import UserSerializer
from follows.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["follower", "followed", "liked_at"]
        read_only_fields = ["liked_at", "follower", "followed"]


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["followed"]

    def validate(self, attrs):
        follower = self.context['request'].user
        followed = attrs.get("followed")
        if follower == followed:
            raise serializers.ValidationError({
                'non_field_errors': ["You cant follow yourself."]
            })

        if Follow.objects.filter(follower=follower, followed=followed).exists():
            raise serializers.ValidationError({
                'non_field_errors': ["You are already following this user."]
            })

        return attrs
