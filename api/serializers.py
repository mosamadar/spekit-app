from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from api.models import (
    Folder,
    Document,
    Topic,
)
from django.db import transaction


class FolderSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = (
            "pk",
            "folder_name",
        )

    def create(self, validated_data):
        """
            Create Folder with the requested data
        """
        with transaction.atomic():
            folder = Folder.create_folder(**validated_data)
        return folder


class DocumentSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = (
            "pk",
            "document_name",
            "folder"
        )

    def create(self, validated_data):
        """
            Create Document within the specified folder id
        """
        with transaction.atomic():
            document = Document.objects.create(**validated_data)
        return document


class TopicsSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = (
            "pk",
            "topic_name",
            "short_description",
            "long_description",
            "document",
        )

    def create(self, validated_data):
        """
            Create Topic within a specified Document
        """
        with transaction.atomic():
            topic = Topic.objects.create(**validated_data)
        return topic


class FindDocumentSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """
        Get The Desired documents with the searchable result provided by user
    """
    folder = serializers.CharField(source="folder.folder_name")

    class Meta:
        model = Document
        fields = (
            "pk",
            "document_name",
            "folder"
        )