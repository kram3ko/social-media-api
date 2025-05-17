from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.views import (
    CreateUserView,
    UserProfileViewSet,
    LogoutUserView,
    MyPofileView,
)

app_name = "accounts"

router = DefaultRouter()
router.register("profile", UserProfileViewSet, basename="profile")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("me/", MyPofileView.as_view(), name="me"),
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
