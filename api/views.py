from api.models import (
    Folder,
    Document,
    Topic
)
from rest_framework import status
from api.serializers import (
    FolderSerializer,
    DocumentSerializer,
    TopicsSerializer,
    FindDocumentSerializer
)
from api.baseview import BaseAPIView
from spekit_app.utils import (
    MessageResponse,
    get_available_documents
)


class FolderApiView(BaseAPIView):
    queryset = Folder
    serializer_class = FolderSerializer

    def get(self, request):
        """
            Get all the folders
        """
        folders = self.queryset.objects.all()
        serializer = self.serializer_class(folders, many=True)

        return self.send_response(
            success=True,
            payload=serializer.data,
            description="Total Folder",
            status_code=status.HTTP_200_OK,
        )


    def post(self, request):
        """
        Add a new folder in the database
        """
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            response = serializer.save()
            if response:
                message = MessageResponse.FOLDER_CREATED.value
            else:
                message = MessageResponse.FOLDER_CREATION_ERROR.value
            return self.send_response(
                success=True,
                code=f"200.",
                status_code=status.HTTP_201_CREATED,
                payload={},
                description=message,
            )
        else:
            return self.send_response(
                code=f"422.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(serializer.errors),
            )


class DocumentApiView(BaseAPIView):
    queryset = Document
    serializer_class = DocumentSerializer

    def get(self, request):
        """
            Get all the Documents
        """
        documents = self.queryset.objects.all()
        serializer = self.serializer_class(documents, many=True)

        return self.send_response(
            success=True,
            payload=serializer.data,
            description="Total Documents",
            status_code=status.HTTP_200_OK,
        )


    def post(self, request):
        """
        Add a new document in the database
        """
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            response = serializer.save()
            if response:
                message = MessageResponse.DOCUMENT_CREATED.value
            else:
                message = MessageResponse.DOCUMENT_CREATION_ERROR.value
            return self.send_response(
                success=True,
                code=f"200.",
                status_code=status.HTTP_201_CREATED,
                payload={},
                description=message,
            )
        else:
            return self.send_response(
                code=f"422.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(serializer.errors),
            )


class TopicApiView(BaseAPIView):
    queryset = Topic
    serializer_class = TopicsSerializer

    def get(self, request):
        """
            Get all the Topics
        """
        topics = self.queryset.objects.all()
        serializer = self.serializer_class(topics, many=True)

        return self.send_response(
            success=True,
            payload=serializer.data,
            description="Total Topis",
            status_code=status.HTTP_200_OK,
        )


    def post(self, request):
        """
            Add a new topic in the database
        """
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            response = serializer.save()
            if response:
                message = MessageResponse.TOPIC_CREATED.value
            else:
                message = MessageResponse.TOPIC_CREATION_ERROR.value
            return self.send_response(
                success=True,
                code=f"200.",
                status_code=status.HTTP_201_CREATED,
                payload={},
                description=message,
            )
        else:
            return self.send_response(
                code=f"422.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(serializer.errors),
            )


class GetDesiredDocuments(BaseAPIView):
    topic_serializer = TopicsSerializer
    document_serializer = FindDocumentSerializer

    def get(self, request):
        """
            Get the user provided params to search the documents
        """
        topic_name = request.query_params.get("topic_name", "")
        folder_name = request.query_params.get("folder_name", "")

        message = None
        if topic_name:
            get_topic = Topic.get_topic(topic_name)
            topic_serializer = self.topic_serializer(get_topic, many=True)

            available_documents = get_available_documents(topic_serializer.data)

            if folder_name:
                get_documents = Document.get_desired_document(available_documents, folder_name)
                document_serializer = self.document_serializer(get_documents, many=True)
                message = document_serializer.data

            return self.send_response(
                success=True,
                code=f"200.",
                status_code=status.HTTP_201_CREATED,
                payload={},
                description=message,
            )
        else:
            return self.send_response(
                code=f"422.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=MessageResponse.MISSING_PARAMS.value,
            )

