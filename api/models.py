from django.db import models


class Log_Created(models.Model):
    """ Abstract model containing common fields."""

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Folder(Log_Created):
    """
        All Available Folders To Store Documents
    """
    folder_name = models.CharField("Folder Name", max_length=30)

    class Meta:
        """
            Get Folders Default by newly created order
        """

        ordering = ["-created_on"]

        """
            Create Indexing Based on Folder Name
        """

        indexes = [
            models.Index(fields=['folder_name'], name="folder_name_idx")
        ]


    def __str__(self):
        """
            Get folder name associated with primary key and Model(Table) Name
        """
        return f"{self.folder_name}__{self.pk}_Folder"


    @classmethod
    def create_folder(cls, folder_name):
        """
            Create a new folder query
        """
        return cls.objects.create(folder_name=folder_name)


class Document(Log_Created):
    """
        All Available Documents In a Specific Folder
    """
    document_name = models.CharField("Document Name", max_length=30)
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="available_documents"
    )

    class Meta:
        """
            Get Documents Default by newly created order
        """
        ordering = ["-created_on"]

        """
            Create Indexing Based on Document Name
        """
        indexes = [
            models.Index(fields=['document_name'], name="document_name_idx")
        ]

    def __str__(self):
        """
            Get document name associated with primary key and Model(Table) Name
        """
        return f"{self.document_name}__{self.pk}_Document"


    @classmethod
    def create_document(cls, data):
        """
            Create a new document in a specific folder
        """
        return cls.objects.create(**data)

    @classmethod
    def get_desired_document(cls, ids, folder_name):
        """
            Filter documents based on multiple document id's in a specified user search given folder
        """
        return cls.objects.filter(pk__in=ids, folder__folder_name=folder_name)


class Topic(Log_Created):
    """
        All Available Topic In a Specific Document Within a Folder
    """
    topic_name = models.CharField("Topic Name", max_length=256)
    short_description = models.CharField("Short Topic Description", max_length=512)
    long_description = models.TextField("Long Topic Description")
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="available_topics"
    )

    class Meta:
        """
            Get Topic Default by newly created order
        """
        ordering = ["-created_on"]

        """
            Create Indexing Based on Topic Name
        """
        indexes = [
            models.Index(fields=['topic_name'], name="topic_name_idx")
        ]

    def __str__(self):
        """
            Get topic name associated with primary key and Model(Table) Name
        """
        return f"{self.topic_name}__{self.pk}_Topic"


    @classmethod
    def create_topic(cls, data):
        """
            Create a new topic in a document within a folder
        """
        return cls.objects.create(**data)


    @classmethod
    def get_topic(cls, topic_name):
        """
            Filter the topic name based on search result
        """
        return cls.objects.filter(topic_name=topic_name)
