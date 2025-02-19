from django.urls import path, include
import django_eventstream

from .views import * 

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", CustomUserListCreateAPIView.as_view(), name="users"),
    path("user/<str:username>/", CustomUserRetrieveUpdateDestroyAPIView.as_view(), name="user"),
    path("matches/", MatchesListCreateAPIView.as_view(), name="matches"),
    path("matches/<int:pk>/", MatchesRetrieveUpdateDestroyAPIView.as_view(), name="match"),
    path("events/", include(django_eventstream.urls), {"channels": ["events"]}),
]
