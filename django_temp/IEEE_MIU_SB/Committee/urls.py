from django.urls import path
from .views import (
    LoginView,
    UserRegistrationView,
    UserProfileView,
    UserUpdateView,
    LogoutView,
    SessionView,
    CommitteeListView
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView, name="logout"),
    path("update/", UserUpdateView.as_view(), name="update_profile"),
    path("session/", SessionView.as_view(), name="session"),
    path("committees/<slug:ses_slug>/", CommitteeListView, name="committee_list"),
]
