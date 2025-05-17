from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.filters import UserProfileFilter
from accounts.models import UserProfile
from accounts.serializers import (
    UserCreateSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from base.generics import CreateAPIView, RetrieveUpdateAPIView

from base.viewsets import ModelViewSet

User = get_user_model()


class CreateUserView(CreateAPIView):
    """ Create a new user. The user will be created with the
     provided username, email, and password."""
    request_serializer_class = UserCreateSerializer
    response_serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class LogoutUserView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Logged out"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.select_related("user")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserProfileFilter
    ordering_fields = ["user__username", "user__email"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "bio",
        "city",
    ]

    request_serializer_class = UserProfileSerializer
    response_serializer_class = UserProfileSerializer

    request_action_serializer_classes = {
        "update": UserProfileUpdateSerializer,
        "partial_update": UserProfileUpdateSerializer,
    }

    action_permission_classes = {
        "create": AllowAny,
        "list": AllowAny,
        "destroy": IsAdminUser,
    }


class MyPofileView(RetrieveUpdateAPIView):
    request_serializer_class = UserProfileUpdateSerializer
    response_serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile
