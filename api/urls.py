"""spekit_app URL Configuration

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
from django.urls import path, include
from api.views import (
    FolderApiView,
    DocumentApiView,
    TopicApiView,
    GetDesiredDocuments
)


urlpatterns = [
    path("folders/", FolderApiView.as_view(), name="folders"),
    path("folders/<int:pk>", FolderApiView.as_view(), name="get-folder"),
    path("documents/", DocumentApiView.as_view(), name="documents"),
    path("documents/<int:pk>", DocumentApiView.as_view(), name="get-document"),
    path("topics/", TopicApiView.as_view(), name="topics"),
    path("topics/<int:pk>", TopicApiView.as_view(), name="get-topic"),
    path("find-documents/", GetDesiredDocuments.as_view(), name="find_documents"),
]
