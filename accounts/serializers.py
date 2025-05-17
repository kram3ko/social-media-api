from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from rest_framework import serializers

from accounts.models import UserProfile

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        label=_("Password"),
        style={"input_type": "password"},
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        min_length=8,
        label=_("Confirm Password"),
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": _("Passwords don't match.")})
        attrs.pop("password2", None)
        return attrs

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        label=_("Password"),
        style={"input_type": "password"},
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password"]

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        if password := validated_data.pop("password", None):
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "photo",
            "birth_date",
            "city",
            "website",
            "created",
            "updated",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        if UserProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError("Profile already exists.")
        validated_data["user"] = user
        return super().create(validated_data)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["bio", "photo", "birth_date", "city", "website"]
        read_only_fields = ["created", "updated"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "profile"]
