from django.urls import path, re_path
from .views import (
    SignUpUser,
    AdminTeamsManagement,
    AdminPlayerManagement
)

urlpatterns = [
    path("sign-up/", SignUpUser.as_view(), name="sign_up_user"),
    re_path(r'^admin-teams/$', AdminTeamsManagement.as_view(), name='admin-all-teams'),
    path("admin-update-team/<int:pk>", AdminTeamsManagement.as_view(), name="admin-update-team"),
    re_path(r'^admin-players/$', AdminPlayerManagement.as_view(), name='admin-all-players'),
    path("admin-update-players/<int:pk>", AdminPlayerManagement.as_view(), name="admin-update-player"),
]
