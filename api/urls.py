"""soccer_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from api.views import (
    TeamApiView,
    PlayerApiView,
    TransferPlayer,
    GetPlayerTransferList,
    BuyPlayer
)


urlpatterns = [
    re_path(r'^team/$', TeamApiView.as_view(), name='get_teams'),
    path("team/<int:pk>", TeamApiView.as_view(), name="update_team"),
    re_path(r'^player/$', PlayerApiView.as_view(), name="get_player"),
    path("player/<int:pk>", PlayerApiView.as_view(), name="update_player"),
    path("transfer-player/", TransferPlayer.as_view(), name="transfer_player"),
    path("transfer-list/", GetPlayerTransferList.as_view(), name="transfer_list"),
    path("buy-player/", BuyPlayer.as_view(), name="buy_player"),
]
