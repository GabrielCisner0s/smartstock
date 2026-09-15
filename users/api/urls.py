from django.urls import path

from .views import (
    LoginView,
    RefreshTokenView,
    RegisterView,
    ProfileView,
)


urlpatterns = [

    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "refresh/",
        RefreshTokenView.as_view(),
        name="refresh",
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

]